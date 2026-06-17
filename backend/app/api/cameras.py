from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera
from app.schemas.camera import CameraResponse

router = APIRouter(prefix="/cameras", tags=["cameras"])


@router.get("", response_model=list[CameraResponse])
def list_cameras(db: Session = Depends(get_db)) -> list[Camera]:
    return list(db.scalars(select(Camera).order_by(Camera.id)))
