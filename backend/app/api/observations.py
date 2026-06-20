from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.event import EventEngineResponse
from app.schemas.observation import EventEngineCreate, ObservationCreate, ObservationResponse
from app.services.evaluator_event_service import create_event_from_evaluation
from app.services.event_engine_service import event_to_engine_dict
from app.services.observation_service import (
    create_observation,
    get_observation_or_none,
    list_observations_for_camera,
    observation_to_response_dict,
)

router = APIRouter(tags=["observations"], dependencies=[Depends(get_current_user)])


def _to_response(observation) -> ObservationResponse:
    return ObservationResponse(**observation_to_response_dict(observation))


@router.post(
    "/observations",
    response_model=ObservationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_observation_endpoint(
    payload: ObservationCreate,
    db: Session = Depends(get_db),
) -> ObservationResponse:
    try:
        observation = create_observation(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return _to_response(observation)


@router.get("/observations/{observation_id}", response_model=ObservationResponse)
def get_observation_endpoint(
    observation_id: str,
    db: Session = Depends(get_db),
) -> ObservationResponse:
    observation = get_observation_or_none(db, observation_id)
    if not observation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy observation")
    return _to_response(observation)


@router.get("/cameras/{camera_id}/observations", response_model=list[ObservationResponse])
def list_camera_observations(
    camera_id: str,
    db: Session = Depends(get_db),
    limit: int = 50,
) -> list[ObservationResponse]:
    try:
        observations = list_observations_for_camera(db, camera_id, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return [_to_response(item) for item in observations]


@router.post(
    "/events/engine",
    response_model=EventEngineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_engine_event(
    payload: EventEngineCreate,
    db: Session = Depends(get_db),
) -> EventEngineResponse:
    try:
        event = create_event_from_evaluation(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return EventEngineResponse(**event_to_engine_dict(db, event))
