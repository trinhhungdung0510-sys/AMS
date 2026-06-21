from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.database.session import get_db
from app.models import Camera, User
from app.schemas.camera_zone import CameraZoneCreate, CameraZoneResponse
from app.services.audit import write_audit_log
from app.services.camera_zone_service import (
    create_camera_zone,
    list_zones_for_camera,
    zone_to_response_dict,
)

router = APIRouter(
    tags=["camera-zones"],
    dependencies=[Depends(get_current_user)],
)


def _to_response(zone) -> CameraZoneResponse:
    return CameraZoneResponse(**zone_to_response_dict(zone))


def _get_camera_or_404(camera_id: str, db: Session) -> Camera:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy camera")
    return camera


@router.get("/cameras/{camera_id}/zones", response_model=list[CameraZoneResponse])
def list_camera_zones(camera_id: str, db: Session = Depends(get_db)) -> list[CameraZoneResponse]:
    _get_camera_or_404(camera_id, db)
    zones = list_zones_for_camera(db, camera_id)
    return [_to_response(zone) for zone in zones]


@router.post(
    "/cameras/{camera_id}/zones",
    response_model=CameraZoneResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_camera_zone_endpoint(
    camera_id: str,
    payload: CameraZoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("zone.manage")),
) -> CameraZoneResponse:
    camera = _get_camera_or_404(camera_id, db)
    try:
        zone = create_camera_zone(db, camera_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    write_audit_log(
        db,
        user_id=current_user.id,
        action="create_zone",
        resource_type="camera_zone",
        resource_id=zone.id,
        farm_id=camera.farm_id,
        metadata={"name": zone.name, "camera_id": camera_id},
    )
    db.commit()
    return _to_response(zone)
