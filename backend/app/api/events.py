from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera
from app.schemas.event import EventEngineResponse, EventResponse
from app.services.event_engine_service import event_to_engine_dict, list_events_for_camera
from app.services.vi_localization import event_to_vi_dict
from sqlalchemy import select

from app.models import Event

router = APIRouter(prefix="/events", tags=["events"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[EventResponse])
def list_events(db: Session = Depends(get_db)) -> list[dict]:
    events = list(db.scalars(select(Event).order_by(Event.occurred_at.desc(), Event.id)))
    return [event_to_vi_dict(db, event) for event in events]


@router.get("/engine", response_model=list[EventEngineResponse])
def list_engine_events(db: Session = Depends(get_db)) -> list[EventEngineResponse]:
    events = list(db.scalars(select(Event).order_by(Event.occurred_at.desc(), Event.id)))
    return [EventEngineResponse(**event_to_engine_dict(db, event)) for event in events]


@router.get("/cameras/{camera_id}/timeline", response_model=list[EventEngineResponse])
def list_camera_timeline(camera_id: str, db: Session = Depends(get_db)) -> list[EventEngineResponse]:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy camera")
    events = list_events_for_camera(db, camera_id)
    return [EventEngineResponse(**event_to_engine_dict(db, event)) for event in events]
