from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera
from app.schemas.camera_zone import CameraZoneCreate, CameraZoneResponse
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
) -> CameraZoneResponse:
    try:
        zone = create_camera_zone(db, camera_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return _to_response(zone)
