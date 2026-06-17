from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import CameraStream
from app.schemas.stream import CameraStreamResponse

router = APIRouter(prefix="/streams", tags=["streams"])


@router.get("", response_model=list[CameraStreamResponse])
def list_streams(db: Session = Depends(get_db)) -> list[CameraStream]:
    return list(db.scalars(select(CameraStream).order_by(CameraStream.id)))
