from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.event_bus import get_event_bus
from app.core.event_bus import event_types as topics
from app.models import Camera, CameraHealth

logger = logging.getLogger(__name__)

STATUS_ONLINE = "ONLINE"
STATUS_OFFLINE = "OFFLINE"
STATUS_DEGRADED = "DEGRADED"

HEARTBEAT_OFFLINE_SECONDS = 120
HEARTBEAT_DEGRADED_SECONDS = 60


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_health_id() -> str:
    return f"CH-{uuid.uuid4().hex[:10].upper()}"


def _publish_status_change(
    camera_id: str,
    previous_status: Optional[str],
    status: str,
    *,
    last_seen_at: str,
    fps: Optional[int] = None,
    bitrate: Optional[float] = None,
) -> None:
    get_event_bus().publish(
        topics.CAMERA_STATUS_CHANGED,
        {
            "topic": topics.CAMERA_STATUS_CHANGED,
            "timestamp": utc_now_iso(),
            "data": {
                "cameraId": camera_id,
                "previousStatus": previous_status,
                "status": status,
                "lastSeenAt": last_seen_at,
                "fps": fps,
                "bitrate": bitrate,
            },
        },
    )


class CameraHealthService:
    def get_health_row(self, db: Session, camera_id: str) -> Optional[CameraHealth]:
        return db.scalar(select(CameraHealth).where(CameraHealth.camera_id == camera_id))

    def record_heartbeat(
        self,
        db: Session,
        camera_id: str,
        *,
        fps: int = 25,
        bitrate: float = 4.0,
        timestamp: Optional[str] = None,
    ) -> CameraHealth:
        camera = db.get(Camera, camera_id)
        if not camera:
            raise ValueError("Không tìm thấy camera")

        now = timestamp or utc_now_iso()
        row = self.get_health_row(db, camera_id)
        previous_status = row.status if row else None
        status = STATUS_ONLINE

        if not row:
            row = CameraHealth(
                id=new_health_id(),
                farm_id=camera.farm_id,
                camera_id=camera_id,
                fps=fps,
                bitrate=bitrate,
                last_seen=now,
                status=status,
            )
            db.add(row)
        else:
            row.fps = fps
            row.bitrate = bitrate
            row.last_seen = now
            row.status = status

        db.commit()
        db.refresh(row)

        if previous_status != status:
            _publish_status_change(
                camera_id,
                previous_status,
                status,
                last_seen_at=now,
                fps=fps,
                bitrate=bitrate,
            )

        return row

    def evaluate_statuses(self, db: Session, *, now: Optional[datetime] = None) -> list[CameraHealth]:
        current = now or datetime.now(timezone.utc)
        updated: list[CameraHealth] = []

        rows = list(db.scalars(select(CameraHealth)))
        for row in rows:
            previous_status = row.status
            try:
                last_seen = datetime.fromisoformat(row.last_seen.replace("Z", "+00:00"))
            except ValueError:
                last_seen = current

            age_seconds = (current - last_seen).total_seconds()
            if age_seconds >= HEARTBEAT_OFFLINE_SECONDS:
                next_status = STATUS_OFFLINE
            elif age_seconds >= HEARTBEAT_DEGRADED_SECONDS:
                next_status = STATUS_DEGRADED
            else:
                next_status = STATUS_ONLINE

            if next_status != row.status:
                row.status = next_status
                db.add(row)
                updated.append(row)
                _publish_status_change(
                    row.camera_id,
                    previous_status,
                    next_status,
                    last_seen_at=row.last_seen,
                    fps=row.fps,
                    bitrate=row.bitrate,
                )

        if updated:
            db.commit()
            for row in updated:
                db.refresh(row)

        return updated


camera_health_service = CameraHealthService()
