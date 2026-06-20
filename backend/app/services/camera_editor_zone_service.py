from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Camera, CameraEditorZone
from app.schemas.camera_editor_zone import CameraEditorZoneCreate, CameraEditorZoneUpdate


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_editor_zone_id() -> str:
    return f"CEZ-{uuid.uuid4().hex[:10].upper()}"


def zone_to_response_dict(zone: CameraEditorZone) -> dict:
    return {
        "id": zone.id,
        "camera_id": zone.camera_id,
        "name": zone.name,
        "type": zone.zone_type,
        "color": zone.color,
        "points": zone.points,
        "created_at": zone.created_at,
    }


def _points_payload(points: list) -> list[dict]:
    return [{"x": float(point.x), "y": float(point.y)} for point in points]


def list_zones_for_camera(db: Session, camera_id: str) -> list[CameraEditorZone]:
    return list(
        db.scalars(
            select(CameraEditorZone)
            .where(CameraEditorZone.camera_id == camera_id)
            .order_by(CameraEditorZone.created_at.desc(), CameraEditorZone.id)
        )
    )


def get_editor_zone_or_none(db: Session, zone_id: str) -> CameraEditorZone | None:
    return db.get(CameraEditorZone, zone_id)


def create_editor_zone(db: Session, camera_id: str, payload: CameraEditorZoneCreate) -> CameraEditorZone:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise ValueError("Không tìm thấy camera")

    zone = CameraEditorZone(
        id=new_editor_zone_id(),
        camera_id=camera_id,
        name=payload.name,
        zone_type=payload.type,
        color=payload.color,
        points=_points_payload(payload.points),
        created_at=utc_now_iso(),
    )
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


def update_editor_zone(db: Session, zone: CameraEditorZone, payload: CameraEditorZoneUpdate) -> CameraEditorZone:
    values = payload.model_dump(exclude_unset=True)
    if "type" in values and values["type"] is not None:
        values["zone_type"] = values.pop("type")
    if "points" in values and values["points"] is not None:
        values["points"] = _points_payload(values["points"])

    for field, value in values.items():
        setattr(zone, field, value)

    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


def delete_editor_zone(db: Session, zone: CameraEditorZone) -> None:
    db.delete(zone)
    db.commit()
