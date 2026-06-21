from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera, CameraHealth
from app.schemas.camera_health import CameraHealthResponse
from app.services.camera_health_service import (
    STATUS_DEGRADED,
    STATUS_OFFLINE,
    STATUS_ONLINE,
    camera_health_service,
)

router = APIRouter(prefix="/camera-health", tags=["camera-health"], dependencies=[Depends(get_current_user)])


class CameraHeartbeatRequest(BaseModel):
    camera_id: str = Field(min_length=1, max_length=20)
    fps: int = Field(default=25, ge=0)
    bitrate: float = Field(default=4.0, ge=0)


@router.get("", response_model=list[CameraHealthResponse])
def list_camera_health(db: Session = Depends(get_db)) -> list[CameraHealth]:
    return list(db.scalars(select(CameraHealth).order_by(CameraHealth.camera_id)))


@router.get("/summary")
def camera_health_summary(db: Session = Depends(get_db)) -> dict:
    health_rows = list(db.scalars(select(CameraHealth)))
    cameras = list(db.scalars(select(Camera).where(Camera.is_active.is_(True))))
    health_by_camera = {row.camera_id: row for row in health_rows}

    online = 0
    offline = 0
    warning = 0

    for camera in cameras:
        row = health_by_camera.get(camera.id)
        status = (row.status if row else camera.status or "").upper()
        if status in {STATUS_ONLINE, "ONLINE"}:
            online += 1
        elif status in {STATUS_DEGRADED, "DEGRADED", "WARNING"}:
            warning += 1
        elif status in {STATUS_OFFLINE, "OFFLINE"} or camera.status == "offline":
            offline += 1
        else:
            online += 1

    return {
        "total": len(cameras),
        "online": online,
        "offline": offline,
        "warning": warning,
    }


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
