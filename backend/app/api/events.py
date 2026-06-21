from app.api.deps import get_current_user
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera
from app.schemas.event import EventEngineResponse, EventResponse, PaginatedEventsResponse
from app.services.event_engine_service import event_to_engine_dict, list_events_for_camera
from app.services.event_query_service import query_events_all, query_events_paginated
from app.services.vi_localization import event_to_vi_dict
from sqlalchemy import select

from app.models import Event

router = APIRouter(prefix="/events", tags=["events"], dependencies=[Depends(get_current_user)])


def _uses_modern_query(
    *,
    page: Optional[int],
    limit: Optional[int],
    event_type: Optional[str],
    camera_id: Optional[str],
    zone_id: Optional[str],
) -> bool:
    return any(value is not None for value in (page, limit, event_type, camera_id, zone_id))


@router.get("")
def list_events(
    page: Optional[int] = Query(default=None, ge=1),
    limit: Optional[int] = Query(default=None, ge=1, le=200),
    eventType: Optional[str] = Query(default=None),
    cameraId: Optional[str] = Query(default=None),
    zoneId: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    if not _uses_modern_query(
        page=page,
        limit=limit,
        event_type=eventType,
        camera_id=cameraId,
        zone_id=zoneId,
    ):
        events = list(db.scalars(select(Event).order_by(Event.occurred_at.desc(), Event.id)))
        return [event_to_vi_dict(db, event) for event in events]

    resolved_page = page or 1
    resolved_limit = limit or 50
    rows, total = query_events_paginated(
        db,
        page=resolved_page,
        limit=resolved_limit,
        event_type=eventType,
        camera_id=cameraId,
        zone_id=zoneId,
    )
    items = [EventEngineResponse(**event_to_engine_dict(db, event)) for event in rows]
    return PaginatedEventsResponse(
        items=items,
        total=total,
        page=resolved_page,
        limit=resolved_limit,
    )


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
