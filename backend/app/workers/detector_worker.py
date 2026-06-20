from __future__ import annotations

import json
import logging
import multiprocessing
import signal
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Optional

from app.core.detectors.yolo_detector_adapter import YoloDetectorAdapter
from app.core.event_bus.event_bus import InMemoryEventBus
from app.database.session import SessionLocal
from app.services.observation_service import create_observation
from app.services.observation_validator import observation_validator
from app.services.pipeline_subscribers import register_pipeline_subscribers
from app.services.runtime_metrics_service import register_metrics_subscribers

logger = logging.getLogger(__name__)


@dataclass
class DetectorWorkerConfig:
    camera_id: str
    video_source: str
    model_path: str = "yolov8n.pt"
    confidence: float = 0.5
    fps_limit: float = 5.0
    prefer_bytetrack: bool = True
    ingest_mode: str = "local"  # local | api
    api_url: str = "http://127.0.0.1:8000"
    api_token: Optional[str] = None
    api_email: Optional[str] = None
    api_password: Optional[str] = None


def _setup_local_runtime() -> None:
    import app.core.event_bus.event_bus as event_bus_module

    event_bus_module._event_bus = InMemoryEventBus()
    register_pipeline_subscribers()
    register_metrics_subscribers()


def _http_json(
    method: str,
    url: str,
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 15.0,
) -> dict[str, Any]:
    body = None
    req_headers = {"Content-Type": "application/json", **(headers or {})}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc


def _resolve_api_token(config: DetectorWorkerConfig) -> str:
    if config.api_token:
        return config.api_token
    if not config.api_email or not config.api_password:
        raise ValueError("API ingest requires --token or --email/--password")

    data = _http_json(
        "POST",
        f"{config.api_url.rstrip('/')}/api/auth/login",
        {"email": config.api_email, "password": config.api_password},
    )
    token = data.get("access_token")
    if not token:
        raise ValueError("Login response missing access_token")
    return token


def _build_ingest_handler(config: DetectorWorkerConfig) -> Callable[[dict[str, Any]], None]:
    if config.ingest_mode == "api":
        token = _resolve_api_token(config)

        def ingest_api(payload: dict[str, Any]) -> None:
            try:
                data = _http_json(
                    "POST",
                    f"{config.api_url.rstrip('/')}/api/observations",
                    payload,
                    headers={"Authorization": f"Bearer {token}"},
                )
                logger.debug("Observation ingested: %s", data.get("id"))
            except Exception:
                logger.exception("Observation API ingest failed")

        return ingest_api

    def ingest_local(payload: dict[str, Any]) -> None:
        db = SessionLocal()
        try:
            validated = observation_validator.validate(payload)
            create_observation(db, validated)
        except Exception:
            logger.exception("Local observation ingest failed")
        finally:
            db.close()

    return ingest_local


def run_detector_worker(config: DetectorWorkerConfig) -> None:
    """Run YOLO detector worker in the current process (separate from FastAPI)."""
    if config.ingest_mode == "local":
        _setup_local_runtime()

    detector = YoloDetectorAdapter(
        camera_id=config.camera_id,
        video_source=config.video_source,
        model_path=config.model_path,
        confidence=config.confidence,
        fps_limit=config.fps_limit,
        prefer_bytetrack=config.prefer_bytetrack,
    )
    ingest = _build_ingest_handler(config)
    detector.on_observation(ingest)

    stop = False

    def _handle_signal(_signum, _frame) -> None:
        nonlocal stop
        stop = True

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    detector.start()
    logger.info(
        "YOLO worker running camera=%s source=%s ingest=%s",
        config.camera_id,
        config.video_source,
        config.ingest_mode,
    )

    try:
        while not stop:
            time.sleep(1.0)
    finally:
        detector.stop()
        logger.info("YOLO worker stopped")


def start_detector_worker_process(config: DetectorWorkerConfig) -> multiprocessing.Process:
    """Spawn detector worker in a dedicated OS process."""
    process = multiprocessing.Process(
        target=run_detector_worker,
        args=(config,),
        name=f"yolo-worker-{config.camera_id}",
        daemon=False,
    )
    process.start()
    return process
