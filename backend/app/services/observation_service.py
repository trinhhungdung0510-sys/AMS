from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Camera, Observation
from app.schemas.observation import ObservationCreate
from app.services.observation_validator import observation_validator
from app.core.event_bus import get_event_bus
from app.core.event_bus.event_types import OBSERVATION_CREATED


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_observation_id() -> str:
    return f"OBS-{uuid.uuid4().hex[:10].upper()}"


def _serialize_objects(objects: list) -> list[dict[str, Any]]:
    serialized = []
    for item in objects:
        if hasattr(item, "model_dump"):
            data = item.model_dump(by_alias=True)
        else:
            data = dict(item)
        serialized.append(data)
    return serialized


def observation_to_response_dict(observation: Observation) -> dict:
    return {
        "id": observation.id,
        "camera_id": observation.camera_id,
        "timestamp": observation.timestamp,
        "source": observation.source,
        "frame_width": observation.frame_width,
        "frame_height": observation.frame_height,
        "objects": observation.objects,
        "schema_version": observation.schema_version,
        "created_at": observation.created_at,
    }


def create_observation(db: Session, payload: ObservationCreate) -> Observation:
    validated = observation_validator.validate(payload.model_dump(by_alias=True))

    camera = db.get(Camera, validated.camera_id)
    if not camera:
        raise ValueError("Không tìm thấy camera")

    now = utc_now_iso()
    observation = Observation(
        id=new_observation_id(),
        camera_id=validated.camera_id,
        timestamp=validated.timestamp,
        source=validated.source,
        frame_width=validated.frame_width,
        frame_height=validated.frame_height,
        objects=_serialize_objects(validated.objects),
        schema_version=validated.schema_version,
        created_at=now,
    )
    db.add(observation)
    db.commit()
    db.refresh(observation)

    get_event_bus().publish(
        OBSERVATION_CREATED,
        {
            "topic": OBSERVATION_CREATED,
            "timestamp": now,
            "data": {"observation": observation_to_response_dict(observation)},
        },
    )

    return observation


def get_observation_or_none(db: Session, observation_id: str) -> Observation | None:
    return db.get(Observation, observation_id)


def list_observations_for_camera(
    db: Session,
    camera_id: str,
    *,
    limit: int = 50,
) -> list[Observation]:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise ValueError("Không tìm thấy camera")

    return list(
        db.scalars(
            select(Observation)
            .where(Observation.camera_id == camera_id)
            .order_by(Observation.timestamp.desc(), Observation.id.desc())
            .limit(limit)
        )
    )
