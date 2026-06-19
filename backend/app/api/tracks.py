from app.api.deps import get_current_user
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import ObjectTrack
from app.schemas.object_track import (
    ObjectTrackIdentifyRequest,
    ObjectTrackResponse,
    ObjectTrackSyncRequest,
)
from app.schemas.person_track import TrackDetailResponse
from app.services.employee_tracking import enrich_track_response, link_track_to_employee, sync_tracks
from app.services.workflow_engine import get_track_detail

router = APIRouter(prefix="/tracks", tags=["camera-tracking"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[ObjectTrackResponse])
def list_tracks(
    camera_id: Optional[str] = Query(default=None),
    employee_id: Optional[str] = Query(default=None),
    object_type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> list[dict]:
    query = select(ObjectTrack).order_by(ObjectTrack.last_seen.desc(), ObjectTrack.id)
    if camera_id:
        query = query.where(ObjectTrack.camera_id == camera_id)
    if employee_id:
        query = query.where(ObjectTrack.employee_id == employee_id)
    if object_type:
        query = query.where(ObjectTrack.object_type == object_type)

    tracks = list(db.scalars(query))
    return [enrich_track_response(db, track) for track in tracks]


@router.get("/{track_id}", response_model=TrackDetailResponse)
def get_track(
    track_id: int,
    camera_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> TrackDetailResponse:
    return TrackDetailResponse(**get_track_detail(db, track_id, camera_id=camera_id))


@router.post("/sync", response_model=list[ObjectTrackResponse])
def sync_camera_tracks(payload: ObjectTrackSyncRequest, db: Session = Depends(get_db)) -> list[dict]:
    synced = sync_tracks(db, payload.tracks)
    db.commit()
    return [enrich_track_response(db, track) for track in synced]


@router.post("/{track_id}/identify", response_model=ObjectTrackResponse)
def identify_track(
    track_id: int,
    payload: ObjectTrackIdentifyRequest,
    db: Session = Depends(get_db),
) -> dict:
    try:
        track = link_track_to_employee(
            db,
            track_id=track_id,
            camera_id=payload.camera_id,
            employee_id=payload.employee_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    db.commit()
    db.refresh(track)
    return enrich_track_response(db, track)
