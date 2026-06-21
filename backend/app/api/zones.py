from __future__ import annotations

from app.api.deps import get_current_user

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.zone_designer_catalog import ATSH_LEVEL_COLORS, ATSH_LEVEL_LABELS, ZONE_DESIGNER_TYPES
from app.core.permissions import require_permission
from app.database.session import get_db
from app.models import User, ZonePolygon
from app.schemas.camera_editor_zone import CameraEditorZoneUpdate
from app.schemas.camera_zone import CameraZoneUpdate
from app.schemas.zone import (
    ZoneClassificationResponse,
    ZonePolygonCreate,
    ZonePolygonResponse,
    ZonePolygonUpdate,
    ZoneTemplateItemResponse,
    ZoneTypeOptionResponse,
)
from app.services.camera_editor_zone_service import (
    delete_editor_zone,
    get_editor_zone_or_none,
    update_editor_zone,
    zone_to_response_dict as editor_zone_to_response_dict,
)
from app.services.camera_zone_service import (
    delete_camera_zone,
    get_camera_zone_or_none,
    update_camera_zone,
    zone_to_response_dict as camera_zone_to_response_dict,
)
from app.services.zone_designer_engine import (
    resolve_color,
    resolve_default_level,
    validate_biosecurity_level,
    validate_zone_type,
    zone_to_response_dict,
)
from app.services.audit import write_audit_log

router = APIRouter(prefix="/zones", tags=["zone-designer"],
    dependencies=[Depends(get_current_user)]
)


def _get_zone_or_404(zone_id: str, db: Session) -> ZonePolygon:
    zone = db.get(ZonePolygon, zone_id)
    if not zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy vùng camera")
    return zone


def _to_response(zone: ZonePolygon) -> ZonePolygonResponse:
    return ZonePolygonResponse(**zone_to_response_dict(zone))


@router.get("/types", response_model=list[ZoneTypeOptionResponse])
def list_zone_types() -> list[ZoneTypeOptionResponse]:
    return [
        ZoneTypeOptionResponse(
            ma_vung=code,
            ten_loai_vung=label,
            cap_atsh_mac_dinh=level,
            muc_atsh=ATSH_LEVEL_LABELS[level],
            mau_sac=ATSH_LEVEL_COLORS[level],
        )
        for code, label, level in ZONE_DESIGNER_TYPES
    ]


@router.get("/classifications", response_model=list[ZoneClassificationResponse])
def list_zone_classifications() -> list[ZoneClassificationResponse]:
    return [
        ZoneClassificationResponse(cap_do=level, ten=label, mau_sac=ATSH_LEVEL_COLORS[level])
        for level, label in ATSH_LEVEL_LABELS.items()
    ]


@router.get("/template", response_model=list[ZoneTemplateItemResponse])
def list_zone_template() -> list[ZoneTemplateItemResponse]:
    return [
        ZoneTemplateItemResponse(
            ma_vung=code,
            ten_vung=label,
            phan_loai_vung=ATSH_LEVEL_LABELS[level],
        )
        for code, label, level in ZONE_DESIGNER_TYPES
    ]


@router.get("", response_model=list[ZonePolygonResponse])
def list_zones(
    camera_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[ZonePolygonResponse]:
    query = select(ZonePolygon).order_by(ZonePolygon.created_at.desc(), ZonePolygon.id)
    if camera_id:
        query = query.where(ZonePolygon.camera_id == camera_id)
    zones = list(db.scalars(query))
    return [_to_response(zone) for zone in zones]


@router.get("/{zone_id}", response_model=ZonePolygonResponse)
def get_zone(zone_id: str, db: Session = Depends(get_db)) -> ZonePolygonResponse:
    return _to_response(_get_zone_or_404(zone_id, db))


@router.post("", response_model=ZonePolygonResponse, status_code=status.HTTP_201_CREATED)
def create_zone(
    payload: ZonePolygonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("zone.manage")),
) -> ZonePolygonResponse:
    try:
        validate_zone_type(payload.zone_type)
        level = resolve_default_level(payload.zone_type, payload.biosecurity_level)
        validate_biosecurity_level(level)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    zone_id = payload.id or f"ZP-{uuid.uuid4().hex[:10].upper()}"
    if db.get(ZonePolygon, zone_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ID vùng đã tồn tại")

    zone = ZonePolygon(
        id=zone_id,
        farm_id=payload.farm_id,
        camera_id=payload.camera_id,
        zone_name=payload.zone_name,
        zone_type=payload.zone_type,
        biosecurity_level=level,
        color=resolve_color(biosecurity_level=level, color=payload.color),
        opacity=payload.opacity,
        description=payload.description,
        polygon_points=payload.polygon_points,
        active=payload.active,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    db.add(zone)
    write_audit_log(
        db,
        user_id=current_user.id,
        action="create_zone",
        resource_type="zone_polygon",
        resource_id=zone.id,
        farm_id=zone.farm_id,
        metadata={"zone_name": zone.zone_name},
    )
    db.commit()
    db.refresh(zone)
    return _to_response(zone)


@router.put("/{zone_id}")
def update_zone(zone_id: str, body: dict = Body(...), db: Session = Depends(get_db)):
    camera_zone = get_camera_zone_or_none(db, zone_id)
    if camera_zone is not None:
        try:
            payload = CameraZoneUpdate.model_validate(body)
            updated = update_camera_zone(db, camera_zone, payload)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
        return camera_zone_to_response_dict(updated)

    editor_zone = get_editor_zone_or_none(db, zone_id)
    if editor_zone is not None:
        try:
            payload = CameraEditorZoneUpdate.model_validate(body)
            updated = update_editor_zone(db, editor_zone, payload)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
        return editor_zone_to_response_dict(updated)

    zone = _get_zone_or_404(zone_id, db)
    payload = ZonePolygonUpdate.model_validate(body)
    values = payload.model_dump(exclude_unset=True)

    try:
        if "zone_type" in values and values["zone_type"] is not None:
            validate_zone_type(values["zone_type"])
        if "biosecurity_level" in values and values["biosecurity_level"] is not None:
            validate_biosecurity_level(values["biosecurity_level"])
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    next_type = values.get("zone_type", zone.zone_type)
    next_level = values.get("biosecurity_level", zone.biosecurity_level)
    if "zone_type" in values and "biosecurity_level" not in values:
        next_level = resolve_default_level(next_type, zone.biosecurity_level)

    if "biosecurity_level" in values or "zone_type" in values:
        values["biosecurity_level"] = next_level

    if "color" not in values and ("biosecurity_level" in values or "zone_type" in values):
        values["color"] = resolve_color(biosecurity_level=next_level, color=zone.color)

    for field, value in values.items():
        setattr(zone, field, value)

    db.add(zone)
    db.commit()
    db.refresh(zone)
    return _to_response(zone)


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_zone(
    zone_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("zone.manage")),
) -> None:
    camera_zone = get_camera_zone_or_none(db, zone_id)
    if camera_zone is not None:
        write_audit_log(
            db,
            user_id=current_user.id,
            action="delete_zone",
            resource_type="camera_zone",
            resource_id=camera_zone.id,
            farm_id=camera_zone.farm_id,
            metadata={"name": camera_zone.name},
        )
        delete_camera_zone(db, camera_zone)
        return

    editor_zone = get_editor_zone_or_none(db, zone_id)
    if editor_zone is not None:
        delete_editor_zone(db, editor_zone)
        return

    zone = _get_zone_or_404(zone_id, db)
    write_audit_log(
        db,
        user_id=current_user.id,
        action="delete_zone",
        resource_type="zone_polygon",
        resource_id=zone.id,
        farm_id=zone.farm_id,
        metadata={"zone_name": zone.zone_name},
    )
    db.delete(zone)
    db.commit()
