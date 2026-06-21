from __future__ import annotations

import asyncio
import logging
import random
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.core.config import get_settings
from app.database.session import SessionLocal
from app.models import Camera, CameraZone
from app.services.demo_assets_service import snapshot_url_for_event_type
from app.services.demo_bootstrap_service import DEMO_CAMERAS, DEMO_FARM_ID, bootstrap_demo_environment
from app.services.demo_data_generator import generate_demo_violations
from app.services.demo_mode_service import is_demo_mode
from app.services.evaluator_event_service import create_compliance_violation_event
from app.services.camera_health_service import camera_health_service

logger = logging.getLogger(__name__)

DEMO_EVENT_TYPES = (
    COMPLIANCE_RULE_IDS["UNIFORM_VIOLATION"],
    COMPLIANCE_RULE_IDS["ZONE_INTRUSION"],
    COMPLIANCE_RULE_IDS["ANIMAL_INTRUSION"],
    COMPLIANCE_RULE_IDS["BIOSECURITY_PROCESS_VIOLATION"],
    COMPLIANCE_RULE_IDS["VEHICLE_INTRUSION"],
)

DEMO_RULE_NAMES = {
    COMPLIANCE_RULE_IDS["UNIFORM_VIOLATION"]: "Sai đồng phục bảo hộ",
    COMPLIANCE_RULE_IDS["ZONE_INTRUSION"]: "Xâm nhập vùng cấm",
    COMPLIANCE_RULE_IDS["ANIMAL_INTRUSION"]: "Động vật xâm nhập",
    COMPLIANCE_RULE_IDS["BIOSECURITY_PROCESS_VIOLATION"]: "Vi phạm quy trình an toàn sinh học",
    COMPLIANCE_RULE_IDS["VEHICLE_INTRUSION"]: "Xe xâm nhập / chưa sát trùng",
}

EVENT_CAMERA_HINTS = {
    COMPLIANCE_RULE_IDS["UNIFORM_VIOLATION"]: "CAM-DEMO-01",
    COMPLIANCE_RULE_IDS["BIOSECURITY_PROCESS_VIOLATION"]: "CAM-DEMO-01",
    COMPLIANCE_RULE_IDS["ZONE_INTRUSION"]: "CAM-DEMO-03",
    COMPLIANCE_RULE_IDS["ANIMAL_INTRUSION"]: "CAM-DEMO-03",
    COMPLIANCE_RULE_IDS["VEHICLE_INTRUSION"]: "CAM-DEMO-02",
}

COMPLIANCE_TARGETS = (85, 90, 95)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class DemoEventGenerator:
    def __init__(self) -> None:
        self._running = False
        self._task: asyncio.Task | None = None
        self._stop_event = asyncio.Event()
        self._events_generated = 0
        self._target_index = 0

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def events_generated(self) -> int:
        return self._events_generated

    def current_compliance_score(self) -> int:
        return COMPLIANCE_TARGETS[self._target_index % len(COMPLIANCE_TARGETS)]

    def _rotate_compliance_target(self) -> None:
        self._target_index = (self._target_index + 1) % len(COMPLIANCE_TARGETS)

    def _pick_demo_camera(self, db: Session, event_type: str) -> tuple[Camera, CameraZone | None]:
        preferred_id = EVENT_CAMERA_HINTS.get(event_type)
        if preferred_id:
            camera = db.get(Camera, preferred_id)
            if camera and camera.is_active:
                zone = db.scalar(
                    select(CameraZone).where(CameraZone.camera_id == camera.id).limit(1)
                )
                return camera, zone

        demo_ids = [item[0] for item in DEMO_CAMERAS]
        cameras = list(
            db.scalars(
                select(Camera).where(
                    Camera.is_active.is_(True),
                    Camera.farm_id == DEMO_FARM_ID,
                    Camera.id.in_(demo_ids),
                )
            )
        )
        if not cameras:
            cameras = list(db.scalars(select(Camera).where(Camera.is_active.is_(True)).limit(5)))
        if not cameras:
            raise ValueError("Không có camera demo để sinh sự kiện")

        camera = random.choice(cameras)
        zone = db.scalar(select(CameraZone).where(CameraZone.camera_id == camera.id).limit(1))
        return camera, zone

    def generate_one(self, db: Session, *, publish: bool = True):
        event_type = random.choice(DEMO_EVENT_TYPES)
        camera, zone = self._pick_demo_camera(db, event_type)
        track_id = random.randint(100, 999)
        score = round(random.uniform(0.62, 0.96), 2)
        zone_id = zone.id if zone else camera.zone

        event = create_compliance_violation_event(
            db,
            event_type=event_type,
            rule_id=event_type.lower(),
            rule_name=DEMO_RULE_NAMES[event_type],
            camera_id=camera.id,
            zone_id=zone_id,
            track_id=track_id,
            score=score,
            snapshot_path=snapshot_url_for_event_type(event_type),
            timestamp=utc_now_iso(),
            evidence={
                "source": "demo_event_generator",
                "demoMode": True,
                "farmId": camera.farm_id,
                "cameraName": camera.name,
            },
            publish=publish,
        )
        self._events_generated += 1
        if self._events_generated % 3 == 0:
            self._rotate_compliance_target()
        try:
            camera_health_service.record_heartbeat(db, camera.id, fps=25, bitrate=2048.0)
        except Exception:
            logger.debug("Demo heartbeat skipped for %s", camera.id)
        return event

    def seed_baseline(self, db: Session, *, count: int, publish: bool = True) -> int:
        bootstrap_demo_environment(db)
        events = generate_demo_violations(
            db,
            count=count,
            publish=publish,
            use_today=True,
            farm_id=DEMO_FARM_ID,
        )
        self._events_generated += len(events)
        return len(events)

    async def start(self) -> None:
        if self._running:
            return
        self._stop_event.clear()
        self._running = True
        self._task = asyncio.create_task(self._worker())
        logger.info("DemoEventGenerator started")

    async def stop(self) -> None:
        if not self._running:
            return
        self._stop_event.set()
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        self._running = False
        logger.info("DemoEventGenerator stopped")

    async def _worker(self) -> None:
        settings = get_settings()
        interval = max(5, settings.demo_interval_seconds)

        db = SessionLocal()
        try:
            if is_demo_mode(db):
                bootstrap_demo_environment(db)
                if self._events_generated == 0:
                    self.seed_baseline(db, count=settings.demo_seed_count, publish=True)
        finally:
            db.close()

        while not self._stop_event.is_set():
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=interval)
                continue
            except asyncio.TimeoutError:
                pass

            db = SessionLocal()
            try:
                if not is_demo_mode(db):
                    continue
                self.generate_one(db, publish=True)
            except Exception:
                logger.exception("Demo event generation failed")
            finally:
                db.close()


demo_event_generator = DemoEventGenerator()
