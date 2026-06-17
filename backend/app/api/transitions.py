import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.realtime import dashboard_manager, manager
from app.database.session import get_db
from app.models import ZoneTransition
from app.schemas.transition import (
    RecentZoneCrossingsResponse,
    ZoneCrossingInput,
    ZoneTransitionCreate,
    ZoneTransitionResponse,
)
from app.services.animal_intrusion_engine import evaluate_animal_intrusion
from app.services.biosecurity_engine import evaluate_transition
from app.services.workflow_engine import evaluate_workflow
from app.services.zone_crossing_engine import process_zone_crossing

router = APIRouter(prefix="/transitions", tags=["zone-transitions"])


@router.get("", response_model=list[ZoneTransitionResponse])
def list_transitions(db: Session = Depends(get_db)) -> list[ZoneTransition]:
    return list(
        db.scalars(
            select(ZoneTransition).order_by(
                ZoneTransition.cross_time.desc(),
                ZoneTransition.id,
            )
        )
    )


@router.get("/recent", response_model=RecentZoneCrossingsResponse)
def list_recent_transitions(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> RecentZoneCrossingsResponse:
    total = db.scalar(select(func.count()).select_from(ZoneTransition)) or 0
    items = list(
        db.scalars(
            select(ZoneTransition)
            .order_by(ZoneTransition.cross_time.desc(), ZoneTransition.id.desc())
            .limit(limit)
        )
    )
    return RecentZoneCrossingsResponse(total=total, items=items)


@router.post("/cross", response_model=ZoneTransitionResponse, responses={204: {"description": "Same zone, no crossing"}})
async def register_zone_crossing(
    payload: ZoneCrossingInput,
    db: Session = Depends(get_db),
):
    try:
        transition = process_zone_crossing(
            db,
            track_id=payload.track_id,
            camera_id=payload.camera_id,
            zone_id=payload.zone_id,
            timestamp=payload.timestamp,
            object_type=payload.object_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    if transition is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    db.flush()
    violation_payload = evaluate_transition(db, transition)
    intrusion_payload = evaluate_animal_intrusion(db, transition)
    workflow_payload = evaluate_workflow(db, transition)
    db.commit()
    db.refresh(transition)

    await dashboard_manager.broadcast(
        {
            "type": "dashboard_update",
            "source": "zone_crossing_engine",
            "transition_id": transition.id,
            "track_id": transition.track_id,
            "camera_id": transition.camera_id,
            "from_zone": transition.from_zone,
            "to_zone": transition.to_zone,
            "cross_time": transition.cross_time,
        }
    )

    if violation_payload:
        await manager.broadcast(violation_payload)
        await dashboard_manager.broadcast(
            {
                "type": "dashboard_update",
                "source": "biosecurity_rule_engine",
                "event_id": violation_payload["event_id"],
            }
        )
    if intrusion_payload:
        await manager.broadcast(intrusion_payload)
        await dashboard_manager.broadcast(
            {
                "type": "dashboard_update",
                "source": "animal_intrusion_engine",
                "event_id": intrusion_payload["event_id"],
            }
        )
    if workflow_payload:
        await manager.broadcast(workflow_payload)
        await dashboard_manager.broadcast(
            {
                "type": "dashboard_update",
                "source": "workflow_engine",
                "event_id": workflow_payload["event_id"],
            }
        )
    return transition


@router.post("", response_model=ZoneTransitionResponse, status_code=status.HTTP_201_CREATED)
async def create_transition(payload: ZoneTransitionCreate, db: Session = Depends(get_db)) -> ZoneTransition:
    cross_time = payload.cross_time or payload.timestamp
    if not cross_time:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="cross_time is required")

    transition = ZoneTransition(
        id=f"ZT-{uuid.uuid4().hex[:12].upper()}",
        object_type=payload.object_type,
        track_id=payload.track_id,
        camera_id=payload.camera_id,
        from_zone=payload.from_zone,
        to_zone=payload.to_zone,
        cross_time=cross_time,
        timestamp=cross_time,
    )
    db.add(transition)
    db.flush()
    violation_payload = evaluate_transition(db, transition)
    intrusion_payload = evaluate_animal_intrusion(db, transition)
    workflow_payload = evaluate_workflow(db, transition)
    db.commit()
    db.refresh(transition)
    if violation_payload:
        await manager.broadcast(violation_payload)
        await dashboard_manager.broadcast(
            {
                "type": "dashboard_update",
                "source": "biosecurity_rule_engine",
                "event_id": violation_payload["event_id"],
            }
        )
    if intrusion_payload:
        await manager.broadcast(intrusion_payload)
        await dashboard_manager.broadcast(
            {
                "type": "dashboard_update",
                "source": "animal_intrusion_engine",
                "event_id": intrusion_payload["event_id"],
            }
        )
    if workflow_payload:
        await manager.broadcast(workflow_payload)
        await dashboard_manager.broadcast(
            {
                "type": "dashboard_update",
                "source": "workflow_engine",
                "event_id": workflow_payload["event_id"],
            }
        )
    return transition
