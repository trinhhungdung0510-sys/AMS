from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import CameraHealth
from app.schemas.camera_health import CameraHealthResponse
from app.services.camera_health_service import camera_health_service

router = APIRouter(prefix="/camera-health", tags=["camera-health"], dependencies=[Depends(get_current_user)])


class CameraHeartbeatRequest(BaseModel):
    camera_id: str = Field(min_length=1, max_length=20)
    fps: int = Field(default=25, ge=0)
    bitrate: float = Field(default=4.0, ge=0)


@router.get("", response_model=list[CameraHealthResponse])
def list_camera_health(db: Session = Depends(get_db)) -> list[CameraHealth]:
    return list(db.scalars(select(CameraHealth).order_by(CameraHealth.camera_id)))


@router.post("/heartbeat", response_model=CameraHealthResponse)
def record_camera_heartbeat(
    payload: CameraHeartbeatRequest,
    db: Session = Depends(get_db),
) -> CameraHealth:
    try:
        return camera_health_service.record_heartbeat(
            db,
            payload.camera_id,
            fps=payload.fps,
            bitrate=payload.bitrate,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
