from app.api.deps import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import CameraHealth
from app.schemas.camera_health import CameraHealthResponse

router = APIRouter(prefix="/camera-health", tags=["camera-health"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[CameraHealthResponse])
def list_camera_health(db: Session = Depends(get_db)) -> list[CameraHealth]:
    return list(db.scalars(select(CameraHealth).order_by(CameraHealth.camera_id)))
