from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.vi_catalog import (
    BIOSECURITY_LEVEL_TO_ZONE_LEVEL,
    EMAIL_FIELD_LABELS,
    SEVERITY_EMAIL_PREFIX,
    SEVERITY_LABELS,
    STATUS_LABELS,
    ZONE_CODE_TO_NAME,
    ZONE_LEVEL_LABELS,
)
from app.models import Camera, Event, Farm, FarmZone
from app.events.event_catalog import enrich_event_fields


class LocalizationCache:
    def __init__(self, db: Session):
        self._db = db
        self._zones: dict[str, str] = {}
        self._cameras: dict[str, str] = {}
        self._farms: dict[str, str] = {}

    def preload_for_events(self, events: list[Event]) -> None:
        zone_codes = {event.zone for event in events if event.zone}
        camera_ids = {event.camera_id for event in events if event.camera_id}
        farm_ids = {event.farm_id for event in events if event.farm_id}

        if zone_codes:
            rows = self._db.scalars(
                select(FarmZone).where(FarmZone.zone_code.in_(tuple(zone_codes)))
            )
            for row in rows:
                self._zones[row.zone_code] = row.name

        if camera_ids:
            rows = self._db.scalars(select(Camera).where(Camera.id.in_(tuple(camera_ids))))
            for row in rows:
                self._cameras[row.id] = row.name

        if farm_ids:
            rows = self._db.scalars(select(Farm).where(Farm.id.in_(tuple(farm_ids))))
            for row in rows:
                self._farms[row.id] = row.name

    def zone_name(self, zone_code: str) -> str:
        if not zone_code:
            return "Không xác định"
        if zone_code in self._zones:
            return self._zones[zone_code]
        name = resolve_zone_name(self._db, zone_code)
        self._zones[zone_code] = name
        return name

    def camera_name(self, camera_id: str) -> str:
        if not camera_id:
            return camera_id
        if camera_id in self._cameras:
            return self._cameras[camera_id]
        name = resolve_camera_name(self._db, camera_id)
        self._cameras[camera_id] = name
        return name

    def farm_name(self, farm_id: str) -> str:
        if not farm_id:
            return farm_id
        if farm_id in self._farms:
            return self._farms[farm_id]
        name = resolve_farm_name(self._db, farm_id)
        self._farms[farm_id] = name
        return name


def resolve_zone_name(db: Session, zone_code: str) -> str:
    if not zone_code:
        return "Không xác định"
    farm_zone = db.scalar(select(FarmZone).where(FarmZone.zone_code == zone_code).limit(1))
    if farm_zone:
        return farm_zone.name
    return ZONE_CODE_TO_NAME.get(zone_code, zone_code)


def resolve_zone_level_label(db: Session, zone_code: str) -> str:
    farm_zone = db.scalar(select(FarmZone).where(FarmZone.zone_code == zone_code).limit(1))
    if farm_zone:
        level = BIOSECURITY_LEVEL_TO_ZONE_LEVEL.get(farm_zone.biosecurity_level, "yellow")
        return ZONE_LEVEL_LABELS[level]
    if zone_code in {"boar_barn", "farrowing_barn", "gestation_barn", "weaning_barn", "fattening_barn", "feed_storage", "vet_medicine_storage", "quarantine_barn"}:
        return ZONE_LEVEL_LABELS["red"]
    if zone_code in {"worker_housing", "cafeteria", "guard_house", "parking_zone", "pig_loading_zone", "farm_gate"}:
        return ZONE_LEVEL_LABELS["orange"]
    if zone_code in {"vehicle_disinfection_zone", "shower_room", "handwash_zone", "supply_storage"}:
        return ZONE_LEVEL_LABELS["yellow"]
    return ZONE_LEVEL_LABELS["green"]


def resolve_severity_label(severity: str) -> str:
    return SEVERITY_LABELS.get(severity.lower(), severity)


def resolve_status_label(status: str) -> str:
    return STATUS_LABELS.get(status, status)


def resolve_farm_name(db: Session, farm_id: str) -> str:
    farm = db.get(Farm, farm_id)
    return farm.name if farm else farm_id


def resolve_camera_name(db: Session, camera_id: str) -> str:
    camera = db.get(Camera, camera_id)
    return camera.name if camera else camera_id


def event_to_vi_dict(db: Session, event: Event, cache: LocalizationCache | None = None) -> dict:
    metadata = event.event_metadata or {}
    score = event.confidence_score
    if score is None and event.confidence is not None:
        score = round(event.confidence / 100, 2)

    zone_name = cache.zone_name(event.zone) if cache else resolve_zone_name(db, event.zone)
    rule_name = metadata.get("rule_name") or event.alert_type
    enriched = enrich_event_fields(
        event_type=event.event_type or event.alert_type,
        category=event.category,
        severity=event.severity,
        rule_name=rule_name,
        zone_name=zone_name,
    )

    return {
        "id": event.id,
        "ten_vi_pham": enriched["title"],
        "muc_do": resolve_severity_label(enriched["severity"]),
        "ten_vung": zone_name,
        "ten_camera": cache.camera_name(event.camera_id) if cache else resolve_camera_name(db, event.camera_id),
        "ten_trang_trai": cache.farm_name(event.farm_id) if cache else resolve_farm_name(db, event.farm_id),
        "do_tin_cay": event.confidence,
        "thoi_gian": event.occurred_at,
        "trang_thai": resolve_status_label(event.status),
        "nguoi_xu_ly": event.handler,
        "event_type": enriched["event_type"],
        "classification": enriched["classification"],
        "severity": enriched["severity"],
        "title": enriched["title"],
        "description": enriched["description"],
        "recommendedAction": enriched["recommendedAction"],
        "explanation": enriched["explanation"],
        "camera_id": event.camera_id,
        "zone_id": event.zone_id,
        "rule_id": event.rule_id or metadata.get("rule_id"),
        "rule_name": rule_name,
        "snapshot_path": event.snapshot_url,
        "score": score,
    }


def events_to_vi_dicts(db: Session, events: list[Event]) -> list[dict]:
    if not events:
        return []
    cache = LocalizationCache(db)
    cache.preload_for_events(events)
    return [event_to_vi_dict(db, event, cache=cache) for event in events]


def build_email_alert(
    *,
    severity: str,
    violation_name: str,
    farm_name: str,
    camera_name: str,
    zone_name: str,
    object_label: str,
    confidence: int,
    occurred_at: str,
    snapshot_url: str = "",
) -> dict:
    prefix = SEVERITY_EMAIL_PREFIX.get(severity.lower(), "CẢNH BÁO")
    subject = f"[{prefix}] {violation_name}"
    body_lines = [
        f"{EMAIL_FIELD_LABELS['farm']}: {farm_name}",
        f"{EMAIL_FIELD_LABELS['camera']}: {camera_name}",
        f"{EMAIL_FIELD_LABELS['zone']}: {zone_name}",
        f"{EMAIL_FIELD_LABELS['violation_type']}: {violation_name}",
        f"{EMAIL_FIELD_LABELS['object']}: {object_label}",
        f"{EMAIL_FIELD_LABELS['confidence']}: {confidence}%",
        f"{EMAIL_FIELD_LABELS['time']}: {occurred_at}",
        f"{EMAIL_FIELD_LABELS['snapshot']}: {snapshot_url or 'Không có'}",
    ]
    return {
        "tieu_de": subject,
        "noi_dung": "\n".join(body_lines),
    }
