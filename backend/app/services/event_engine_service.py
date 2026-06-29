from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Camera, CameraZone, Event, ZoneRule
from app.events.event_catalog import enrich_event_fields
from app.services.vi_localization import LocalizationCache, resolve_severity_label


class EngineDictCache:
    def __init__(self, db: Session):
        self._db = db
        self._localization = LocalizationCache(db)
        self._camera_zones: dict[str, CameraZone] = {}
        self._rules: dict[str, ZoneRule] = {}

    def preload_for_events(self, events: list[Event]) -> None:
        self._localization.preload_for_events(events)
        zone_ids = {event.zone_id for event in events if event.zone_id}
        rule_ids = {event.rule_id for event in events if event.rule_id}

        if zone_ids:
            rows = self._db.scalars(select(CameraZone).where(CameraZone.id.in_(tuple(zone_ids))))
            for row in rows:
                self._camera_zones[row.id] = row

        if rule_ids:
            rows = self._db.scalars(select(ZoneRule).where(ZoneRule.id.in_(tuple(rule_ids))))
            for row in rows:
                self._rules[row.id] = row

    def build(self, event: Event) -> dict:
        zone_name = event.zone
        if event.zone_id:
            zone = self._camera_zones.get(event.zone_id)
            if zone:
                zone_name = zone.name

        rule_name = None
        if event.rule_id:
            rule = self._rules.get(event.rule_id)
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
            "farm_id": event.farm_id,
            "category": event.category,
            "camera_id": event.camera_id,
            "camera_name": self._localization.camera_name(event.camera_id),
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


def event_to_engine_dict(db: Session, event: Event) -> dict:
    cache = EngineDictCache(db)
    cache.preload_for_events([event])
    return cache.build(event)


def events_to_engine_dicts(db: Session, events: list[Event]) -> list[dict]:
    if not events:
        return []
    cache = EngineDictCache(db)
    cache.preload_for_events(events)
    return [cache.build(event) for event in events]


def list_events_for_camera(db: Session, camera_id: str) -> list[Event]:
    return list(
        db.scalars(
            select(Event)
            .where(Event.camera_id == camera_id)
            .order_by(Event.occurred_at.desc(), Event.id)
        )
    )
