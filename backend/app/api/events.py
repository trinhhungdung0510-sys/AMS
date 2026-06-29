from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models import Camera, Event
from app.schemas.event import EventEngineResponse, PaginatedEventsResponse
from app.services.event_engine_service import event_to_engine_dict, events_to_engine_dicts, list_events_for_camera
from app.services.event_query_service import query_events_paginated

router = APIRouter(prefix="/events", tags=["events"], dependencies=[Depends(get_current_user)])

DEFAULT_EVENT_PAGE_SIZE = 100


@router.get("")
def list_events(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=DEFAULT_EVENT_PAGE_SIZE, ge=1, le=200),
    eventType: Optional[str] = Query(default=None),
    cameraId: Optional[str] = Query(default=None),
    zoneId: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> PaginatedEventsResponse:
    rows, total = query_events_paginated(
        db,
        page=page,
        limit=limit,
        event_type=eventType,
        camera_id=cameraId,
        zone_id=zoneId,
    )
    items = [EventEngineResponse(**item) for item in events_to_engine_dicts(db, rows)]
    return PaginatedEventsResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
    )


@router.get("/engine", response_model=list[EventEngineResponse])
def list_engine_events(
    limit: int = Query(default=DEFAULT_EVENT_PAGE_SIZE, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[EventEngineResponse]:
    rows, _ = query_events_paginated(db, page=1, limit=limit)
    return [EventEngineResponse(**item) for item in events_to_engine_dicts(db, rows)]


@router.get("/cameras/{camera_id}/timeline", response_model=list[EventEngineResponse])
def list_camera_timeline(camera_id: str, db: Session = Depends(get_db)) -> list[EventEngineResponse]:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy camera")
    events = list_events_for_camera(db, camera_id)
    return [EventEngineResponse(**event_to_engine_dict(db, event)) for event in events]
