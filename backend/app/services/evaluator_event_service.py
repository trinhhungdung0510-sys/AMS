from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Camera, CameraZone, Event, ZoneRule
from app.schemas.observation import EventEngineCreate

EVENT_STATUS_OPEN = "OPEN"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_event_id() -> str:
    return f"EVT-{uuid.uuid4().hex[:10].upper()}"


def create_event_from_evaluation(db: Session, payload: EventEngineCreate) -> Event:
    camera = db.get(Camera, payload.camera_id)
    rule = db.get(ZoneRule, payload.rule_id)
    zone = db.get(CameraZone, payload.zone_id)

    if not camera:
        raise ValueError("Không tìm thấy camera")
    if not rule or rule.camera_id != payload.camera_id:
        raise ValueError("Rule không hợp lệ")
    if not rule.enabled:
        raise ValueError("Rule đang tắt (disabled)")
    if not zone or zone.camera_id != payload.camera_id:
        raise ValueError("Zone không hợp lệ")

    score = payload.confidence_score if payload.confidence_score is not None else 0.9
    now = utc_now_iso()
    metadata = dict(payload.event_metadata or {})
    metadata.setdefault("source", "evaluator_engine")
    metadata.setdefault("rule_name", rule.name)
    metadata.setdefault("zone_name", zone.name)
    if payload.observation_id:
        metadata["observation_id"] = payload.observation_id

    event = Event(
        id=new_event_id(),
        farm_id=camera.farm_id,
        camera_id=payload.camera_id,
        category="rule_engine",
        alert_type=rule.name,
        zone=zone.name,
        severity=payload.severity,
        status=EVENT_STATUS_OPEN,
        handler="Chưa phân công",
        confidence=int(round(score * 100)),
        occurred_at=now,
        zone_id=payload.zone_id,
        rule_id=payload.rule_id,
        event_type=payload.event_type,
        confidence_score=score,
        snapshot_url=None,
        started_at=now,
        ended_at=None,
        event_metadata=metadata,
        record_created_at=now,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
