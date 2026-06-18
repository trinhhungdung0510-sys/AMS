"""AMS v4.0 ATSH Biosecurity AI Engine — evaluates 5 core ATSH rules on zone transitions."""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.biosecurity_ai_v40 import (
    CLEAN_BIOSECURITY_LEVELS,
    DIRTY_BIOSECURITY_LEVELS,
    FEED_TRUCK_OBJECT_TYPES,
    FEED_TRUCK_ZONES,
    PIG_TRUCK_OBJECT_TYPES,
    PIG_TRUCK_ZONES,
    PRODUCTION_BARN_CODES,
    RESTRICTED_BIOSECURITY_LEVELS,
    SANITATION_ZONE_CODES,
    normalize_atsh_severity,
)
from app.data.farm_template import PRODUCTION_ZONE_CODES
from app.data.animal_intrusion import ANIMAL_OBJECT_TYPES
from app.models import BiosecurityRule, Camera, Event, FarmZone, ObjectTrack, ZonePolygon, ZoneTransition
from app.services.audit import write_audit_log
from app.services.snapshot_generator import SnapshotAnnotation, create_event_snapshot
from app.services.vi_localization import build_email_alert, resolve_camera_name, resolve_farm_name, resolve_zone_name

DEFAULT_CAMERA_ID = "CAM-001"
ATSH_EVENT_CATEGORY = "atsh_violation"


def evaluate_atsh_biosecurity(db: Session, transition: ZoneTransition) -> Optional[dict]:
    rules = list(
        db.scalars(
            select(BiosecurityRule)
            .where(BiosecurityRule.enabled.is_(True))
            .where(BiosecurityRule.rule_type.is_not(None))
            .order_by(BiosecurityRule.id)
        )
    )
    if not rules:
        return None

    from_meta = _resolve_zone_meta(db, transition.from_zone)
    to_meta = _resolve_zone_meta(db, transition.to_zone)

    for rule in rules:
        violation = _evaluate_rule(db, transition, rule, from_meta, to_meta)
        if violation:
            transition.atsh_rule_code = rule.rule_code
            transition.atsh_severity = violation["severity"]
            db.add(transition)
            return violation
    return None


def create_atsh_violation_event(
    db: Session,
    *,
    rule: BiosecurityRule,
    transition: Optional[ZoneTransition],
    camera_id: str,
    zone_code: str,
    object_type: str,
    track_id: Optional[int] = None,
    occurred_at: str,
    confidence: int = 99,
) -> dict:
    camera = db.get(Camera, camera_id) or db.get(Camera, DEFAULT_CAMERA_ID)
    severity = normalize_atsh_severity(rule.severity)
    event_id = f"EVT-ATSH-{uuid.uuid4().hex[:8].upper()}"
    snapshot_id = f"SNP-ATSH-{uuid.uuid4().hex[:8].upper()}"
    alert_type = f"Vi phạm ATSH: {rule.rule_name_vi}"[:120]

    event = Event(
        id=event_id,
        farm_id=camera.farm_id if camera else "FARM-001",
        camera_id=camera.id if camera else camera_id,
        category=ATSH_EVENT_CATEGORY,
        alert_type=alert_type,
        zone=zone_code,
        severity=severity.lower(),
        status="new",
        handler="Chưa phân công",
        confidence=confidence,
        occurred_at=occurred_at,
        violation_code=rule.rule_code,
    )
    snapshot = create_event_snapshot(
        event_id=event_id,
        snapshot_id=snapshot_id,
        storage_category="biosecurity",
        annotation=SnapshotAnnotation(
            object_label=object_type,
            zone_name=resolve_zone_name(db, zone_code),
            rule_name=rule.rule_name_vi,
            timestamp=occurred_at,
            severity=severity.lower(),
            track_id=track_id,
            confidence=confidence,
        ),
    )
    db.add(event)
    db.add(snapshot)

    metadata = {
        "rule_id": rule.id,
        "rule_code": rule.rule_code,
        "rule_type": rule.rule_type,
        "evaluation_mode": rule.evaluation_mode,
        "severity": severity,
        "event_id": event_id,
        "snapshot_id": snapshot_id,
        "object_type": object_type,
        "zone_code": zone_code,
    }
    if transition:
        metadata.update(
            {
                "transition_id": transition.id,
                "track_id": transition.track_id,
                "from_zone": transition.from_zone,
                "to_zone": transition.to_zone,
            }
        )
        if track_id is None:
            track_id = transition.track_id

    write_audit_log(
        db,
        user_id="SYSTEM",
        action="atsh_biosecurity_violation",
        resource_type="zone_transition" if transition else "ai_detection",
        resource_id=transition.id if transition else event_id,
        metadata=metadata,
    )

    farm_id = camera.farm_id if camera else "FARM-001"
    email_alert = build_email_alert(
        severity=severity.lower(),
        violation_name=rule.rule_name_vi,
        farm_name=resolve_farm_name(db, farm_id),
        camera_name=resolve_camera_name(db, camera.id if camera else camera_id),
        zone_name=resolve_zone_name(db, zone_code),
        object_label=object_type,
        confidence=confidence,
        occurred_at=occurred_at,
        snapshot_url=f"/storage/biosecurity/{event_id}.jpg",
    )

    return {
        "type": "atsh_violation",
        "rule_id": rule.id,
        "rule_code": rule.rule_code,
        "rule_type": rule.rule_type,
        "ten_vi_pham": rule.rule_name_vi,
        "muc_do": severity,
        "severity": severity,
        "event_id": event_id,
        "snapshot_id": snapshot_id,
        "transition_id": transition.id if transition else None,
        "object_type": object_type,
        "track_id": track_id,
        "from_zone": transition.from_zone if transition else None,
        "to_zone": transition.to_zone if transition else zone_code,
        "occurred_at": occurred_at,
        "email": email_alert,
        "notification": {
            "email": True,
            "telegram": severity == "CRITICAL",
            "zalo": severity == "CRITICAL",
        },
    }


def get_atsh_violation_summary(db: Session) -> dict:
    events = list(
        db.scalars(select(Event).where(Event.category == ATSH_EVENT_CATEGORY))
    )
    from datetime import datetime, timezone

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    counts = {"INFO": 0, "WARNING": 0, "CRITICAL": 0, "total": 0, "hom_nay": 0}
    by_rule: dict[str, int] = {}

    for event in events:
        severity = normalize_atsh_severity(event.severity)
        counts[severity] = counts.get(severity, 0) + 1
        counts["total"] += 1
        if event.occurred_at.startswith(today):
            counts["hom_nay"] += 1
        code = event.violation_code or event.alert_type
        by_rule[code] = by_rule.get(code, 0) + 1

    top_rules = sorted(
        ({"ma_quy_tac": code, "so_vi_pham": total} for code, total in by_rule.items()),
        key=lambda item: item["so_vi_pham"],
        reverse=True,
    )[:5]

    return {
        "tong_vi_pham_atsh": counts["total"],
        "vi_pham_hom_nay": counts["hom_nay"],
        "theo_muc_do": {
            "INFO": counts.get("INFO", 0),
            "WARNING": counts.get("WARNING", 0),
            "CRITICAL": counts.get("CRITICAL", 0),
        },
        "top_quy_tac": top_rules,
    }


def _evaluate_rule(
    db: Session,
    transition: ZoneTransition,
    rule: BiosecurityRule,
    from_meta: dict,
    to_meta: dict,
) -> Optional[dict]:
    rule_type = (rule.rule_type or "").lower()
    if rule_type == "forbidden_zone_intrusion":
        return _eval_forbidden_zone(db, transition, rule, to_meta)
    if rule_type == "animal_intrusion_clean_zone":
        return _eval_animal_clean_zone(db, transition, rule, to_meta)
    if rule_type == "dirty_to_clean_movement":
        return _eval_dirty_to_clean(db, transition, rule, from_meta, to_meta)
    if rule_type == "worker_contact_pig_truck":
        return _eval_worker_contact(db, transition, rule, truck_zones=PIG_TRUCK_ZONES, truck_types=PIG_TRUCK_OBJECT_TYPES)
    if rule_type == "worker_contact_feed_truck":
        return _eval_worker_contact(db, transition, rule, truck_zones=FEED_TRUCK_ZONES, truck_types=FEED_TRUCK_OBJECT_TYPES)
    return None


def _eval_forbidden_zone(
    db: Session,
    transition: ZoneTransition,
    rule: BiosecurityRule,
    to_meta: dict,
) -> Optional[dict]:
    if transition.object_type.lower() != "person":
        return None

    to_level = to_meta.get("biosecurity_level", "")
    to_zone = transition.to_zone
    is_restricted = (
        to_level in RESTRICTED_BIOSECURITY_LEVELS
        or to_zone in {"feed_storage", "vet_medicine_storage", "quarantine_barn"}
    )
    if not is_restricted:
        return None

    return create_atsh_violation_event(
        db,
        rule=rule,
        transition=transition,
        camera_id=transition.camera_id,
        zone_code=to_zone,
        object_type=transition.object_type,
        occurred_at=transition.cross_time,
    )


def _eval_animal_clean_zone(
    db: Session,
    transition: ZoneTransition,
    rule: BiosecurityRule,
    to_meta: dict,
) -> Optional[dict]:
    object_type = transition.object_type.lower()
    if object_type not in ANIMAL_OBJECT_TYPES:
        return None

    to_level = to_meta.get("biosecurity_level", "")
    to_zone = transition.to_zone
    is_clean = to_level in CLEAN_BIOSECURITY_LEVELS or to_zone in PRODUCTION_BARN_CODES
    if not is_clean:
        return None

    return create_atsh_violation_event(
        db,
        rule=rule,
        transition=transition,
        camera_id=transition.camera_id,
        zone_code=to_zone,
        object_type=object_type,
        occurred_at=transition.cross_time,
    )


def _eval_dirty_to_clean(
    db: Session,
    transition: ZoneTransition,
    rule: BiosecurityRule,
    from_meta: dict,
    to_meta: dict,
) -> Optional[dict]:
    if transition.object_type.lower() != "person":
        return None

    from_level = from_meta.get("biosecurity_level", "")
    to_level = to_meta.get("biosecurity_level", "")
    from_zone = transition.from_zone
    to_zone = transition.to_zone

    from_dirty = from_level in DIRTY_BIOSECURITY_LEVELS or from_zone in {
        "worker_housing",
        "cafeteria",
        "parking_zone",
        "pig_loading_zone",
        "reception_zone",
    }
    to_clean = to_level in CLEAN_BIOSECURITY_LEVELS or to_zone in PRODUCTION_ZONE_CODES

    if not from_dirty or not to_clean:
        return None
    if from_zone in SANITATION_ZONE_CODES or to_zone in SANITATION_ZONE_CODES:
        return None
    if _track_has_sanitation_between(db, transition.track_id, transition.cross_time):
        return None

    return create_atsh_violation_event(
        db,
        rule=rule,
        transition=transition,
        camera_id=transition.camera_id,
        zone_code=to_zone,
        object_type=transition.object_type,
        occurred_at=transition.cross_time,
    )


def _eval_worker_contact(
    db: Session,
    transition: ZoneTransition,
    rule: BiosecurityRule,
    *,
    truck_zones: set[str],
    truck_types: set[str],
) -> Optional[dict]:
    if transition.object_type.lower() != "person":
        return None
    if transition.to_zone not in truck_zones:
        return None

    truck_present = db.scalar(
        select(ObjectTrack.id)
        .where(ObjectTrack.camera_id == transition.camera_id)
        .where(ObjectTrack.current_zone == transition.to_zone)
        .where(ObjectTrack.object_type.in_(tuple(truck_types)))
        .where(ObjectTrack.leave_time.is_(None))
        .limit(1)
    )
    if not truck_present:
        return None

    return create_atsh_violation_event(
        db,
        rule=rule,
        transition=transition,
        camera_id=transition.camera_id,
        zone_code=transition.to_zone,
        object_type=transition.object_type,
        occurred_at=transition.cross_time,
    )


def _resolve_zone_meta(db: Session, zone_code: str) -> dict:
    farm_zone = db.scalar(select(FarmZone).where(FarmZone.zone_code == zone_code).limit(1))
    if farm_zone:
        return {
            "zone_category": farm_zone.zone_category,
            "biosecurity_level": farm_zone.biosecurity_level,
            "risk_level": farm_zone.risk_level,
        }

    polygon = db.scalar(select(ZonePolygon).where(ZonePolygon.zone_type == zone_code).limit(1))
    if polygon:
        level_map = {"red": "restricted", "orange": "dirty", "yellow": "neutral", "green": "clean"}
        return {"biosecurity_level": level_map.get(polygon.biosecurity_level, polygon.biosecurity_level)}

    return {}


def _track_has_sanitation_between(db: Session, track_id: int, before: str) -> bool:
    return (
        db.scalar(
            select(ZoneTransition.id)
            .where(ZoneTransition.track_id == track_id)
            .where(ZoneTransition.cross_time < before)
            .where(ZoneTransition.to_zone.in_(tuple(SANITATION_ZONE_CODES)))
            .limit(1)
        )
        is not None
    )
