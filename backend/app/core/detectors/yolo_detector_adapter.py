from __future__ import annotations

import logging
import threading
import time
from typing import Any, Optional

from app.core.detectors.capabilities import (
    DETECTOR_STATUS_DEGRADED,
    DETECTOR_STATUS_FAILED,
    DETECTOR_STATUS_RUNNING,
    DETECTOR_STATUS_STARTING,
    DETECTOR_STATUS_STOPPED,
    DetectorCapabilities,
)
from app.core.detectors.detector_adapter import BaseDetectorAdapter
from app.core.detectors.yolo_class_mapper import SUPPORTED_COCO_CLASS_IDS, map_coco_class_id
from app.core.detectors.yolo_observation_mapper import (
    build_observation_object,
    build_observation_payload,
    normalize_bbox_xyxy,
)
from app.core.detectors.yolo_tracker import DetectionInput, create_tracker, is_bytetrack_available
from app.core.event_bus import get_event_bus
from app.core.event_bus import event_types as topics
from app.services.observation_service import utc_now_iso

logger = logging.getLogger(__name__)


def parse_video_source(source: str) -> str | int:
    """Accept rtsp:// URL, video file path, webcam index, or 'webcam'."""
    cleaned = source.strip()
    lowered = cleaned.lower()
    if lowered in {"webcam", "cam", "camera"}:
        return 0
    if lowered.startswith("webcam:"):
        return int(cleaned.split(":", 1)[1])
    if cleaned.isdigit():
        return int(cleaned)
    return cleaned


class YoloDetectorAdapter(BaseDetectorAdapter):
    """Ultralytics YOLO detector — person + dog/cat/bird (mapped to animal)."""

    def __init__(
        self,
        *,
        camera_id: str,
        video_source: str,
        model_path: str = "yolov8n.pt",
        confidence: float = 0.5,
        fps_limit: float = 5.0,
        prefer_bytetrack: bool = True,
    ) -> None:
        super().__init__(
            name="yolo-detector-v1",
            source="YOLO",
            capabilities=DetectorCapabilities(
                person_detection=True,
                animal_detection=True,
                ppe_detection=False,
                tracking=True,
            ),
        )
        self._camera_id = camera_id
        self._video_source_raw = video_source
        self._video_source = parse_video_source(video_source)
        self._model_path = model_path
        self._confidence = confidence
        self._fps_limit = max(0.1, fps_limit)
        self._prefer_bytetrack = prefer_bytetrack
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._model: Any = None
        self._capture: Any = None
        self._tracker: Any = None
        self._frames_processed = 0
        self._last_frame_at: Optional[str] = None
        self._tracking_backend = "simple"

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        self._health.status = DETECTOR_STATUS_STARTING
        self._health.message = "Loading YOLO model"
        self._publish_detector_event(topics.DETECTOR_STARTED)

        try:
            self._load_runtime()
        except Exception as exc:
            self._health.status = DETECTOR_STATUS_FAILED
            self._health.last_error = str(exc)
            self._health.message = "Failed to start YOLO detector"
            self._publish_detector_event(topics.DETECTOR_FAILED, error=str(exc))
            raise

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, name="yolo-detector", daemon=True)
        self._thread.start()
        self._health.status = DETECTOR_STATUS_RUNNING
        self._health.started_at = utc_now_iso()
        self._health.message = f"YOLO running ({self._tracking_backend})"

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
        self._release_capture()
        self._health.status = DETECTOR_STATUS_STOPPED
        self._health.stopped_at = utc_now_iso()
        self._health.message = "YOLO detector stopped"
        self._publish_detector_event(topics.DETECTOR_STOPPED)

    def health(self):
        extra_message = self._health.message
        if self._frames_processed:
            extra_message = (
                f"{extra_message}; frames={self._frames_processed}; backend={self._tracking_backend}"
            )
        self._health.message = extra_message
        return self._health

    def get_capabilities(self) -> DetectorCapabilities:
        caps = super().get_capabilities()
        caps.tracking = True
        return caps

    def _load_runtime(self) -> None:
        import cv2
        from ultralytics import YOLO

        self._model = YOLO(self._model_path)
        self._capture = cv2.VideoCapture(self._video_source)
        if not self._capture.isOpened():
            raise RuntimeError(f"Cannot open video source: {self._video_source_raw}")

        if isinstance(self._video_source, str) and self._video_source.startswith("rtsp"):
            self._capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self._tracker = create_tracker(prefer_bytetrack=self._prefer_bytetrack)
        self._tracking_backend = getattr(self._tracker, "backend_name", "simple")
        if self._prefer_bytetrack and not is_bytetrack_available():
            self._health.status = DETECTOR_STATUS_DEGRADED
            self._health.message = "ByteTrack unavailable; using simple tracker"

    def _release_capture(self) -> None:
        if self._capture is not None:
            try:
                self._capture.release()
            except Exception:
                logger.exception("Failed releasing video capture")
            self._capture = None

    def _run_loop(self) -> None:
        min_interval = 1.0 / self._fps_limit
        last_emit = 0.0

        while not self._stop_event.is_set():
            loop_start = time.perf_counter()
            try:
                ok, frame = self._capture.read()
                if not ok or frame is None:
                    self._health.message = "Waiting for frame"
                    time.sleep(0.2)
                    continue

                self._frames_processed += 1
                self._last_frame_at = utc_now_iso()
                frame_height, frame_width = frame.shape[:2]

                results = self._model.predict(
                    frame,
                    conf=self._confidence,
                    classes=list(SUPPORTED_COCO_CLASS_IDS),
                    verbose=False,
                )
                result = results[0]
                names = result.names

                detections: list[DetectionInput] = []
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        cls_id = int(box.cls.item())
                        ams_class = map_coco_class_id(cls_id, names)
                        if not ams_class:
                            continue
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        detections.append(
                            DetectionInput(
                                x1=float(x1),
                                y1=float(y1),
                                x2=float(x2),
                                y2=float(y2),
                                confidence=float(box.conf.item()),
                                class_name=str(names.get(cls_id, "")),
                            )
                        )

                tracked = self._tracker.update(detections)
                now = time.perf_counter()
                if tracked and (now - last_emit) >= min_interval:
                    objects = [
                        build_observation_object(
                            track_id=item.track_id,
                            object_class=item.ams_class,
                            confidence=item.confidence,
                            bbox=normalize_bbox_xyxy(
                                item.x1,
                                item.y1,
                                item.x2,
                                item.y2,
                                frame_width,
                                frame_height,
                            ),
                            attributes={"tracker": item.tracker},
                        )
                        for item in tracked
                    ]
                    payload = build_observation_payload(
                        camera_id=self._camera_id,
                        objects=objects,
                        frame_width=frame_width,
                        frame_height=frame_height,
                        source=self.source,
                    )
                    self._emit_observation(payload)
                    last_emit = now
            except Exception as exc:
                logger.exception("YOLO inference loop error")
                self._health.last_error = str(exc)
                self._health.message = f"Inference error: {exc}"
                self._publish_detector_event(topics.DETECTOR_FAILED, error=str(exc))
                time.sleep(1.0)

            elapsed = time.perf_counter() - loop_start
            sleep_for = min_interval - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)

        self._release_capture()

    def _publish_detector_event(self, topic: str, **extra: Any) -> None:
        get_event_bus().publish(
            topic,
            {
                "topic": topic,
                "timestamp": utc_now_iso(),
                "data": {"detectorName": self.name, "cameraId": self._camera_id, **extra},
            },
        )
