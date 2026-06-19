from app.api.deps import get_current_user
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Visitor
from app.schemas.visitor import (
    VisitorCheckInRequest,
    VisitorCheckOutRequest,
    VisitorCreate,
    VisitorResponse,
    VisitorUpdate,
)

router = APIRouter(prefix="/visitors", tags=["visitors"],
    dependencies=[Depends(get_current_user)]
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _visitor_status(visitor: Visitor) -> str:
    if visitor.arrival_time and not visitor.departure_time:
        return "checked_in"
    if visitor.arrival_time and visitor.departure_time:
        return "checked_out"
    return "scheduled"


def _to_response(visitor: Visitor) -> VisitorResponse:
    return VisitorResponse(
        id=visitor.id,
        visitor_name=visitor.visitor_name,
        company=visitor.company,
        vehicle_plate=visitor.vehicle_plate,
        visit_purpose=visitor.visit_purpose,
        arrival_time=visitor.arrival_time,
        departure_time=visitor.departure_time,
        approved_by=visitor.approved_by,
        status=_visitor_status(visitor),
    )


def _get_visitor_or_404(visitor_id: str, db: Session) -> Visitor:
    visitor = db.get(Visitor, visitor_id)
    if not visitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")
    return visitor


@router.get("", response_model=list[VisitorResponse])
def list_visitors(
    company: Optional[str] = Query(default=None),
    status_filter: Optional[str] = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
) -> list[VisitorResponse]:
    visitors = list(db.scalars(select(Visitor).order_by(Visitor.arrival_time.desc(), Visitor.id)))
    if company:
        visitors = [visitor for visitor in visitors if visitor.company == company]
    if status_filter:
        visitors = [visitor for visitor in visitors if _visitor_status(visitor) == status_filter]
    return [_to_response(visitor) for visitor in visitors]


@router.get("/{visitor_id}", response_model=VisitorResponse)
def get_visitor(visitor_id: str, db: Session = Depends(get_db)) -> VisitorResponse:
    return _to_response(_get_visitor_or_404(visitor_id, db))


@router.post("", response_model=VisitorResponse, status_code=status.HTTP_201_CREATED)
def create_visitor(payload: VisitorCreate, db: Session = Depends(get_db)) -> VisitorResponse:
    visitor_id = payload.id or f"VIS-{uuid.uuid4().hex[:8].upper()}"
    if db.get(Visitor, visitor_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Visitor id already exists")

    visitor = Visitor(
        id=visitor_id,
        visitor_name=payload.visitor_name,
        company=payload.company,
        vehicle_plate=payload.vehicle_plate,
        visit_purpose=payload.visit_purpose,
        arrival_time=payload.arrival_time,
        departure_time=payload.departure_time,
        approved_by=payload.approved_by,
    )
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return _to_response(visitor)


@router.put("/{visitor_id}", response_model=VisitorResponse)
def update_visitor(
    visitor_id: str,
    payload: VisitorUpdate,
    db: Session = Depends(get_db),
) -> VisitorResponse:
    visitor = _get_visitor_or_404(visitor_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(visitor, field, value)
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return _to_response(visitor)


@router.delete("/{visitor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_visitor(visitor_id: str, db: Session = Depends(get_db)) -> None:
    visitor = _get_visitor_or_404(visitor_id, db)
    db.delete(visitor)
    db.commit()


@router.post("/{visitor_id}/check-in", response_model=VisitorResponse)
def check_in_visitor(
    visitor_id: str,
    payload: VisitorCheckInRequest,
    db: Session = Depends(get_db),
) -> VisitorResponse:
    visitor = _get_visitor_or_404(visitor_id, db)
    if visitor.arrival_time and not visitor.departure_time:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Visitor is already checked in")

    visitor.arrival_time = payload.arrival_time or _now_iso()
    visitor.departure_time = None
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return _to_response(visitor)


@router.post("/{visitor_id}/check-out", response_model=VisitorResponse)
def check_out_visitor(
    visitor_id: str,
    payload: VisitorCheckOutRequest,
    db: Session = Depends(get_db),
) -> VisitorResponse:
    visitor = _get_visitor_or_404(visitor_id, db)
    if not visitor.arrival_time:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Visitor has not checked in yet")
    if visitor.departure_time:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Visitor is already checked out")

    visitor.departure_time = payload.departure_time or _now_iso()
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return _to_response(visitor)
