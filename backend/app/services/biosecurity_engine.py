import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import BiosecurityRule, Camera, Event, FarmZone, ZoneTransition
from app.services.atsh_biosecurity_engine import evaluate_atsh_biosecurity
from app.services.audit import write_audit_log
from app.services.snapshot_generator import SnapshotAnnotation, create_event_snapshot
from app.services.vi_localization import build_email_alert, resolve_camera_name, resolve_farm_name, resolve_zone_name

DEFAULT_CAMERA_ID = "CAM-001"


def evaluate_transition(db: Session, transition: ZoneTransition) -> Optional[dict]:
    atsh_violation = evaluate_atsh_biosecurity(db, transition)
    if atsh_violation:
        return atsh_violation

    rule = _match_legacy_rule(db, transition)
    if not rule:
        return None

    camera = db.get(Camera, transition.camera_id) or db.get(Camera, DEFAULT_CAMERA_ID)
    to_zone_meta = _lookup_zone_metadata(db, transition.to_zone)
    event_id = f"EVT-BIO-{uuid.uuid4().hex[:8].upper()}"
    snapshot_id = f"SNP-BIO-{uuid.uuid4().hex[:8].upper()}"
    alert_type = f"Vi phạm ATSH: {rule.rule_name_vi}"[:80]

    event = Event(
        id=event_id,
        farm_id=camera.farm_id if camera else "FARM-001",
        camera_id=camera.id if camera else transition.camera_id,
        category="atsh_violation",
        alert_type=alert_type,
        zone=transition.to_zone,
        severity=rule.severity,
        status="new",
        handler="Chưa phân công",
        confidence=99,
        occurred_at=transition.cross_time,
        violation_code=rule.rule_code,
    )
    snapshot = create_event_snapshot(
        event_id=event_id,
        snapshot_id=snapshot_id,
        storage_category="biosecurity",
        annotation=SnapshotAnnotation(
            object_label=transition.object_type,
            zone_name=resolve_zone_name(db, transition.to_zone),
            rule_name=rule.rule_name_vi,
            timestamp=transition.cross_time,
            severity=rule.severity,
            track_id=transition.track_id,
            confidence=99,
        ),
    )

    db.add(event)
    db.add(snapshot)
    write_audit_log(
        db,
        user_id="SYSTEM",
        action="biosecurity_rule_violation",
        resource_type="zone_transition",
        resource_id=transition.id,
        metadata={
            "rule_id": rule.id,
            "rule_code": rule.rule_code,
            "object_type": rule.object_type,
            "required_zone": rule.required_zone,
            "event_id": event_id,
            "snapshot_id": snapshot_id,
            "track_id": transition.track_id,
            "from_zone": transition.from_zone,
            "to_zone": transition.to_zone,
            "zone_category": to_zone_meta.get("zone_category"),
            "biosecurity_level": to_zone_meta.get("biosecurity_level"),
            "risk_level": to_zone_meta.get("risk_level"),
        },
    )

    farm_id = camera.farm_id if camera else "FARM-001"
    email_alert = build_email_alert(
        severity=rule.severity,
        violation_name=rule.rule_name_vi,
        farm_name=resolve_farm_name(db, farm_id),
        camera_name=resolve_camera_name(db, camera.id if camera else transition.camera_id),
        zone_name=resolve_zone_name(db, transition.to_zone),
        object_label=transition.object_type,
        confidence=99,
        occurred_at=transition.cross_time,
        snapshot_url=f"/storage/biosecurity/{event_id}.jpg",
    )

    return {
        "type": "atsh_violation",
        "rule_id": rule.id,
        "rule_code": rule.rule_code,
        "ten_vi_pham": rule.rule_name_vi,
        "muc_do": rule.severity,
        "event_id": event_id,
        "snapshot_id": snapshot_id,
        "transition_id": transition.id,
        "object_type": transition.object_type,
        "track_id": transition.track_id,
        "from_zone": transition.from_zone,
        "to_zone": transition.to_zone,
        "zone_category": to_zone_meta.get("zone_category"),
        "biosecurity_level": to_zone_meta.get("biosecurity_level"),
        "risk_level": to_zone_meta.get("risk_level"),
        "occurred_at": transition.cross_time,
        "email": email_alert,
        "notification": {
            "email": True,
            "telegram": rule.severity in {"critical", "high", "CRITICAL"},
            "zalo": rule.severity in {"critical", "CRITICAL"},
        },
    }


def _match_legacy_rule(db: Session, transition: ZoneTransition) -> Optional[BiosecurityRule]:
    rules = list(db.scalars(select(BiosecurityRule).where(BiosecurityRule.enabled.is_(True))))
    object_type = transition.object_type.lower()

    for rule in rules:
        if rule.rule_type is not None:
            continue
        if rule.object_type in (None, "catalog"):
            continue
        if rule.object_type.lower() != object_type:
            continue
        if rule.from_zone and rule.from_zone != "any_zone" and transition.from_zone != rule.from_zone:
            continue
        if rule.to_zone and transition.to_zone != rule.to_zone:
            continue
        if rule.required_zone and _track_has_visited_zone(
            db,
            transition.track_id,
            rule.required_zone,
            before=transition.cross_time,
        ):
            continue
        return rule

    return None


def _lookup_zone_metadata(db: Session, zone_code: str) -> dict:
    farm_zone = db.scalar(select(FarmZone).where(FarmZone.zone_code == zone_code).limit(1))
    if farm_zone:
        return {
            "zone_category": farm_zone.zone_category,
            "biosecurity_level": farm_zone.biosecurity_level,
            "risk_level": farm_zone.risk_level,
        }
    return {}


def _track_has_visited_zone(db: Session, track_id: int, zone: str, *, before: str) -> bool:
    return (
        db.scalar(
            select(ZoneTransition)
            .where(ZoneTransition.track_id == track_id)
            .where(ZoneTransition.cross_time < before)
            .where((ZoneTransition.from_zone == zone) | (ZoneTransition.to_zone == zone))
            .limit(1)
        )
        is not None
    )
