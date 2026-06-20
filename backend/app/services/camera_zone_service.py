from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Camera, CameraZone
from app.models.camera_zone import POINTS_FORMAT_NORMALIZED, POINTS_FORMAT_PIXEL
from app.schemas.camera_zone import CameraZoneCreate, CameraZoneUpdate
from app.utils.zone_geometry import (
    is_legacy_pixel_zone,
    resolve_normalized_points,
    scale_polygon_to_normalized,
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_camera_zone_id() -> str:
    return f"CZ-{uuid.uuid4().hex[:10].upper()}"


def zone_to_response_dict(zone: CameraZone) -> dict:
    normalized_points = resolve_normalized_points(
        zone.points,
        points_format=zone.points_format,
        reference_width=zone.reference_width,
        reference_height=zone.reference_height,
    )

    return {
        "id": zone.id,
        "camera_id": zone.camera_id,
        "parent_zone_id": zone.parent_zone_id,
        "name": zone.name,
        "description": zone.description,
        "type": zone.zone_type,
        "color": zone.color,
        "points": normalized_points,
        "reference_width": zone.reference_width,
        "reference_height": zone.reference_height,
        "points_format": zone.points_format,
        "created_at": zone.created_at,
        "updated_at": zone.updated_at,
    }


def _points_payload(points: list) -> list[dict]:
    return [{"x": float(point.x), "y": float(point.y)} for point in points]


def _resolve_storage(
    points: list[dict],
    reference_width: Optional[int],
    reference_height: Optional[int],
) -> tuple[list[dict], str, Optional[int], Optional[int]]:
    raw_points = [{"x": float(point["x"]), "y": float(point["y"])} for point in points]

    if not is_legacy_pixel_zone(raw_points):
        if not reference_width or not reference_height:
            raise ValueError("reference_width và reference_height bắt buộc khi points chuẩn hóa")
        return raw_points, POINTS_FORMAT_NORMALIZED, reference_width, reference_height

    if reference_width and reference_height:
        normalized = scale_polygon_to_normalized(raw_points, reference_width, reference_height)
        return normalized, POINTS_FORMAT_NORMALIZED, reference_width, reference_height

    return raw_points, POINTS_FORMAT_PIXEL, reference_width, reference_height


def _validate_parent(db: Session, camera_id: str, parent_zone_id: Optional[str]) -> None:
    if parent_zone_id is None:
        return

    parent = db.get(CameraZone, parent_zone_id)
    if not parent or parent.camera_id != camera_id:
        raise ValueError("Zone cha không tồn tại hoặc không thuộc camera này")
    if parent.parent_zone_id is not None:
        raise ValueError("SubZone chỉ có thể thuộc Zone chính (một cấp)")


def list_zones_for_camera(db: Session, camera_id: str) -> list[CameraZone]:
    return list(
        db.scalars(
            select(CameraZone)
            .where(CameraZone.camera_id == camera_id)
            .order_by(CameraZone.created_at.asc(), CameraZone.id)
        )
    )


def get_camera_zone_or_none(db: Session, zone_id: str) -> CameraZone | None:
    return db.get(CameraZone, zone_id)


def create_camera_zone(db: Session, camera_id: str, payload: CameraZoneCreate) -> CameraZone:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise ValueError("Không tìm thấy camera")

    _validate_parent(db, camera_id, payload.parent_zone_id)

    raw_points = _points_payload(payload.points)
    stored_points, points_format, reference_width, reference_height = _resolve_storage(
        raw_points,
        payload.reference_width,
        payload.reference_height,
    )

    now = utc_now_iso()
    zone = CameraZone(
        id=new_camera_zone_id(),
        camera_id=camera_id,
        parent_zone_id=payload.parent_zone_id,
        name=payload.name,
        description=(payload.description or "").strip() or None,
        zone_type=payload.type,
        color=payload.color,
        points=stored_points,
        reference_width=reference_width,
        reference_height=reference_height,
        points_format=points_format,
        created_at=now,
        updated_at=now,
    )
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


def update_camera_zone(db: Session, zone: CameraZone, payload: CameraZoneUpdate) -> CameraZone:
    values = payload.model_dump(exclude_unset=True)

    if "type" in values and values["type"] is not None:
        values["zone_type"] = values.pop("type")
    if "description" in values:
        values["description"] = (values["description"] or "").strip() or None

    if "points" in values and values["points"] is not None:
        raw_points = _points_payload(values.pop("points"))
        reference_width = values.pop("reference_width", zone.reference_width)
        reference_height = values.pop("reference_height", zone.reference_height)
        stored_points, points_format, reference_width, reference_height = _resolve_storage(
            raw_points,
            reference_width,
            reference_height,
        )
        values["points"] = stored_points
        values["points_format"] = points_format
        values["reference_width"] = reference_width
        values["reference_height"] = reference_height
    else:
        values.pop("reference_width", None)
        values.pop("reference_height", None)

    if "parent_zone_id" in values:
        next_parent = values["parent_zone_id"]
        if next_parent == zone.id:
            raise ValueError("Zone không thể là cha của chính nó")
        _validate_parent(db, zone.camera_id, next_parent)

        if next_parent is not None:
            has_children = db.scalars(
                select(CameraZone.id).where(CameraZone.parent_zone_id == zone.id).limit(1)
            ).first()
            if has_children is not None:
                raise ValueError("Zone đang có SubZone, không thể chuyển thành SubZone")

    for field, value in values.items():
        setattr(zone, field, value)

    zone.updated_at = utc_now_iso()
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


def delete_camera_zone(db: Session, zone: CameraZone) -> None:
    children = list(
        db.scalars(select(CameraZone).where(CameraZone.parent_zone_id == zone.id))
    )
    for child in children:
        db.delete(child)
    db.delete(zone)
    db.commit()
