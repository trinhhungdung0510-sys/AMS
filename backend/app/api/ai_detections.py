from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera
from app.schemas.ai_detection import AiDetectionCreate, AiDetectionResponse
from app.services.ai_detection_service import (
    create_detection,
    detection_to_response_dict,
    list_detections_for_camera,
)

router = APIRouter(
    tags=["ai-detections"],
    dependencies=[Depends(get_current_user)],
)


def _to_response(detection) -> AiDetectionResponse:
    return AiDetectionResponse(**detection_to_response_dict(detection))


def _get_camera_or_404(camera_id: str, db: Session) -> Camera:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy camera")
    return camera


@router.get("/cameras/{camera_id}/detections", response_model=list[AiDetectionResponse])
def list_camera_detections(camera_id: str, db: Session = Depends(get_db)) -> list[AiDetectionResponse]:
    _get_camera_or_404(camera_id, db)
    detections = list_detections_for_camera(db, camera_id)
    return [_to_response(detection) for detection in detections]


@router.post(
    "/cameras/{camera_id}/detections",
    response_model=AiDetectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_camera_detection(
    camera_id: str,
    payload: AiDetectionCreate,
    db: Session = Depends(get_db),
) -> AiDetectionResponse:
    try:
        detection = create_detection(db, camera_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return _to_response(detection)
