from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import Camera, CameraZone, Event, ZoneRule
from app.events.event_catalog import enrich_event_fields
from app.services.vi_localization import (
    event_to_vi_dict,
    resolve_camera_name,
    resolve_severity_label,
)


def event_to_engine_dict(db: Session, event: Event) -> dict:
    zone_name = event.zone
    if event.zone_id:
        zone = db.get(CameraZone, event.zone_id)
        if zone:
            zone_name = zone.name

    rule_name = None
    if event.rule_id:
        rule = db.get(ZoneRule, event.rule_id)
        if rule:
            rule_name = rule.name

    metadata = event.event_metadata or {}
    if not rule_name:
        rule_name = metadata.get("rule_name") or event.alert_type

    confidence = event.confidence_score
    if confidence is None and event.confidence is not None:
        confidence = round(event.confidence / 100, 2)

    score = confidence
    snapshot_path = event.snapshot_url

    enriched = enrich_event_fields(
        event_type=event.event_type or event.alert_type,
        category=event.category,
        severity=event.severity,
        rule_name=rule_name,
        zone_name=zone_name,
    )

    return {
        "id": event.id,
        "camera_id": event.camera_id,
        "camera_name": resolve_camera_name(db, event.camera_id),
        "zone_id": event.zone_id,
        "zone_name": zone_name,
        "rule_id": event.rule_id or metadata.get("rule_id"),
        "rule_name": rule_name,
        "event_type": enriched["event_type"],
        "classification": enriched["classification"],
        "confidence": confidence,
        "score": score,
        "snapshot_url": event.snapshot_url,
        "snapshotPath": snapshot_path,
        "ruleId": event.rule_id or metadata.get("rule_id"),
        "ruleName": rule_name,
        "started_at": event.started_at or event.occurred_at,
        "ended_at": event.ended_at,
        "status": event.status,
        "severity": enriched["severity"],
        "severityLabel": resolve_severity_label(enriched["severity"]),
        "title": enriched["title"],
        "description": enriched["description"],
        "recommendedAction": enriched["recommendedAction"],
        "explanation": enriched["explanation"],
        "metadata": metadata,
        "created_at": event.record_created_at or event.occurred_at,
    }


def list_events_for_camera(db: Session, camera_id: str) -> list[Event]:
    from sqlalchemy import select

    return list(
        db.scalars(
            select(Event)
            .where(Event.camera_id == camera_id)
            .order_by(Event.occurred_at.desc(), Event.id)
        )
    )
