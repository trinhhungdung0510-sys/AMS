from __future__ import annotations

import random
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Camera, CameraZone, Event, ZoneRule

EVENT_STATUS_OPEN = "OPEN"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_event_id() -> str:
    return f"EVT-{uuid.uuid4().hex[:10].upper()}"


def trigger_rule(db: Session, rule_id: str, *, confidence: float | None = None) -> Event:
    rule = db.get(ZoneRule, rule_id)
    if not rule:
        raise ValueError("Không tìm thấy rule")
    if not rule.enabled:
        raise ValueError("Rule đang tắt (disabled)")

    camera = db.get(Camera, rule.camera_id)
    zone = db.get(CameraZone, rule.zone_id)
    if not camera or not zone:
        raise ValueError("Camera hoặc zone không hợp lệ")

    score = confidence if confidence is not None else round(random.uniform(0.85, 0.99), 2)
    now = utc_now_iso()

    event = Event(
        id=new_event_id(),
        farm_id=camera.farm_id,
        camera_id=rule.camera_id,
        category="rule_engine",
        alert_type=rule.name,
        zone=zone.name,
        severity=rule.severity,
        status=EVENT_STATUS_OPEN,
        handler="Chưa phân công",
        confidence=int(round(score * 100)),
        occurred_at=now,
        zone_id=rule.zone_id,
        rule_id=rule.id,
        event_type=rule.rule_type,
        confidence_score=score,
        snapshot_url=None,
        started_at=now,
        ended_at=None,
        event_metadata={
            "source": "mock_rule_engine",
            "rule_name": rule.name,
            "zone_name": zone.name,
        },
        record_created_at=now,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
