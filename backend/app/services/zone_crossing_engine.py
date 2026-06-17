import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.farm_template import TEMPLATE_ZONE_CODES
from app.models import ObjectTrack, ZonePolygon, ZoneTransition


def resolve_zone_code(db: Session, zone_id: str) -> str:
    polygon = db.get(ZonePolygon, zone_id)
    if polygon:
        return polygon.zone_type

    if zone_id in TEMPLATE_ZONE_CODES or zone_id == "unknown":
        return zone_id

    exists = db.scalar(select(ZonePolygon.id).where(ZonePolygon.zone_type == zone_id).limit(1))
    if exists:
        return zone_id

    raise ValueError(f"Zone not found: {zone_id}")


def get_current_zone(db: Session, *, track_id: int, camera_id: str) -> Optional[str]:
    track_key = f"TRK-{camera_id}-{track_id}"
    object_track = db.get(ObjectTrack, track_key)
    if object_track and object_track.current_zone not in {None, "unknown"}:
        return object_track.current_zone

    last_transition = db.scalar(
        select(ZoneTransition)
        .where(ZoneTransition.track_id == track_id)
        .where(ZoneTransition.camera_id == camera_id)
        .order_by(ZoneTransition.cross_time.desc(), ZoneTransition.id.desc())
        .limit(1)
    )
    if last_transition:
        return last_transition.to_zone
    return None


def process_zone_crossing(
    db: Session,
    *,
    track_id: int,
    camera_id: str,
    zone_id: str,
    timestamp: str,
    object_type: Optional[str] = None,
) -> Optional[ZoneTransition]:
    to_zone = resolve_zone_code(db, zone_id)
    from_zone = get_current_zone(db, track_id=track_id, camera_id=camera_id) or "unknown"

    if from_zone == to_zone:
        return None

    resolved_object_type = object_type or _resolve_object_type(db, track_id=track_id, camera_id=camera_id)

    transition = ZoneTransition(
        id=f"ZT-{uuid.uuid4().hex[:12].upper()}",
        track_id=track_id,
        camera_id=camera_id,
        object_type=resolved_object_type,
        from_zone=from_zone,
        to_zone=to_zone,
        cross_time=timestamp,
        timestamp=timestamp,
    )
    db.add(transition)
    _sync_object_track_zone(
        db,
        track_id=track_id,
        camera_id=camera_id,
        object_type=resolved_object_type,
        current_zone=to_zone,
        previous_zone=from_zone if from_zone != "unknown" else None,
        timestamp=timestamp,
    )
    return transition


def _resolve_object_type(db: Session, *, track_id: int, camera_id: str) -> str:
    track_key = f"TRK-{camera_id}-{track_id}"
    object_track = db.get(ObjectTrack, track_key)
    if object_track:
        return object_track.object_type

    last_transition = db.scalar(
        select(ZoneTransition)
        .where(ZoneTransition.track_id == track_id)
        .where(ZoneTransition.camera_id == camera_id)
        .order_by(ZoneTransition.cross_time.desc())
        .limit(1)
    )
    if last_transition:
        return last_transition.object_type
    return "person"


def _sync_object_track_zone(
    db: Session,
    *,
    track_id: int,
    camera_id: str,
    object_type: str,
    current_zone: str,
    previous_zone: Optional[str],
    timestamp: str,
) -> None:
    track_key = f"TRK-{camera_id}-{track_id}"
    track = db.get(ObjectTrack, track_key)
    if track is None:
        track = ObjectTrack(
            id=track_key,
            track_id=track_id,
            camera_id=camera_id,
            object_type=object_type,
            current_zone=current_zone,
            previous_zone=previous_zone,
            employee_id=None,
            enter_time=timestamp,
            leave_time=None,
            last_seen=timestamp,
            confidence=0.0,
        )
    else:
        track.object_type = object_type
        track.previous_zone = previous_zone
        track.current_zone = current_zone
        track.last_seen = timestamp
    db.add(track)
