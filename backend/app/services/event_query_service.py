from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Event


def apply_event_filters(
    query,
    *,
    event_type: str | None = None,
    camera_id: str | None = None,
    zone_id: str | None = None,
    event_types: set[str] | None = None,
    date_prefix: str | None = None,
    since_iso: str | None = None,
    categories: set[str] | None = None,
):
    if event_types:
        query = query.where(Event.event_type.in_(tuple(event_types)))
    if categories:
        query = query.where(Event.category.in_(tuple(categories)))
    if event_type:
        query = query.where(Event.event_type == event_type)
    if camera_id:
        query = query.where(Event.camera_id == camera_id)
    if zone_id:
        query = query.where(Event.zone_id == zone_id)
    if date_prefix:
        query = query.where(Event.occurred_at.startswith(date_prefix))
    if since_iso:
        query = query.where(Event.occurred_at >= since_iso)
    return query


def query_events_paginated(
    db: Session,
    *,
    page: int = 1,
    limit: int = 50,
    event_type: str | None = None,
    camera_id: str | None = None,
    zone_id: str | None = None,
    event_types: set[str] | None = None,
    date_prefix: str | None = None,
    since_iso: str | None = None,
    categories: set[str] | None = None,
) -> tuple[list[Event], int]:
    base = select(Event)
    base = apply_event_filters(
        base,
        event_type=event_type,
        camera_id=camera_id,
        zone_id=zone_id,
        event_types=event_types,
        date_prefix=date_prefix,
        since_iso=since_iso,
        categories=categories,
    )

    count_query = select(func.count()).select_from(base.subquery())
    total = db.scalar(count_query) or 0

    offset = max(page - 1, 0) * limit
    rows = db.scalars(
        base.order_by(Event.occurred_at.desc(), Event.id).offset(offset).limit(limit)
    )
    return list(rows), int(total)


def query_events_all(
    db: Session,
    *,
    event_type: str | None = None,
    camera_id: str | None = None,
    zone_id: str | None = None,
    event_types: set[str] | None = None,
    date_prefix: str | None = None,
    since_iso: str | None = None,
    categories: set[str] | None = None,
) -> list[Event]:
    query = select(Event)
    query = apply_event_filters(
        query,
        event_type=event_type,
        camera_id=camera_id,
        zone_id=zone_id,
        event_types=event_types,
        date_prefix=date_prefix,
        since_iso=since_iso,
        categories=categories,
    )
    return list(db.scalars(query.order_by(Event.occurred_at.desc(), Event.id)))
