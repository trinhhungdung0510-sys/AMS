from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Camera, CameraZone, Event, ZoneRule
from app.schemas.observation import EventEngineCreate
from app.core.event_bus import get_event_bus
from app.core.event_bus.event_types import EVENT_CREATED
from app.services.event_engine_service import event_to_engine_dict
from app.events.event_catalog import enrich_event_fields, resolve_event_severity

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

    get_event_bus().publish(
        EVENT_CREATED,
        {
            "topic": EVENT_CREATED,
            "timestamp": now,
            "data": {"event": event_to_engine_dict(db, event)},
        },
    )

    return event


COMPLIANCE_EVENT_CATEGORY = "compliance_violation"


def create_compliance_violation_event(
    db: Session,
    *,
    event_type: str,
    rule_id: str,
    rule_name: str,
    camera_id: str,
    zone_id: str,
    track_id: int | None,
    score: float,
    snapshot_path: str | None,
    timestamp: str | None = None,
    evidence: dict | None = None,
    publish: bool = True,
) -> Event:
    camera = db.get(Camera, camera_id)
    zone = db.get(CameraZone, zone_id) if zone_id else None
    now = timestamp or utc_now_iso()
    metadata = dict(evidence or {})
    zone_name = getattr(zone, "name", None) if zone else zone_id
    resolved_severity = resolve_event_severity(event_type, fallback=_compliance_score_to_severity(score))
    enriched = enrich_event_fields(
        event_type=event_type,
        category=COMPLIANCE_EVENT_CATEGORY,
        severity=resolved_severity,
        rule_name=rule_name,
        zone_name=zone_name or zone_id,
    )
    metadata.update(
        {
            "source": "compliance_engine",
            "rule_id": rule_id,
            "rule_name": rule_name,
            "event_type": event_type,
            "track_id": track_id,
            "score": score,
            "classification": enriched["classification"],
            "title": enriched["title"],
            "description": enriched["description"],
            "recommendedAction": enriched["recommendedAction"],
        }
    )

    event = Event(
        id=new_event_id(),
        farm_id=camera.farm_id if camera else "FARM-001",
        camera_id=camera_id,
        category=COMPLIANCE_EVENT_CATEGORY,
        alert_type=enriched["title"],
        zone=zone_name or zone_id,
        severity=enriched["severity"],
        status=EVENT_STATUS_OPEN,
        handler="Chưa phân công",
        confidence=int(round(score * 100)),
        occurred_at=now,
        zone_id=zone_id or None,
        rule_id=rule_id,
        event_type=event_type,
        confidence_score=score,
        snapshot_url=snapshot_path,
        started_at=now,
        ended_at=None,
        event_metadata=metadata,
        record_created_at=utc_now_iso(),
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    if publish:
        get_event_bus().publish(
            EVENT_CREATED,
            {
                "topic": EVENT_CREATED,
                "timestamp": utc_now_iso(),
                "data": {"event": event_to_engine_dict(db, event)},
            },
        )

    return event


def _compliance_score_to_severity(score: float) -> str:
    if score >= 0.9:
        return "HIGH"
    if score >= 0.7:
        return "MEDIUM"
    return "LOW"
