from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Event
from app.schemas.event import EventResponse
from app.services.vi_localization import event_to_vi_dict

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventResponse])
def list_events(db: Session = Depends(get_db)) -> list[dict]:
    events = list(db.scalars(select(Event).order_by(Event.occurred_at.desc(), Event.id)))
    return [event_to_vi_dict(db, event) for event in events]
