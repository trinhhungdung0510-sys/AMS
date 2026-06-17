import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.animal_intrusion import ANIMAL_OBJECT_TYPES, ZONE_ALIASES
from app.models import AnimalIntrusionPolicy, Camera, Event, FarmZone, ZoneTransition
from app.services.audit import write_audit_log
from app.services.snapshot_generator import SnapshotAnnotation, create_event_snapshot, resolve_zone_display_name

DEFAULT_CAMERA_ID = "CAM-001"

ANIMAL_VIOLATION_LABELS = {
    "dog": "Chó xâm nhập khu chăn nuôi",
    "cat": "Mèo xâm nhập khu chăn nuôi",
    "rat": "Chuột xuất hiện trong khu vực sản xuất",
    "bird": "Chim xuất hiện trong kho cám",
}


def _violation_label(object_type: str, zone_code: str) -> str:
    if object_type == "bird" or zone_code in {"feed_storage", "feed_storage_zone"}:
        return ANIMAL_VIOLATION_LABELS["bird"]
    return ANIMAL_VIOLATION_LABELS.get(object_type, f"Động vật xâm nhập {zone_code}")


def normalize_zone_code(zone_code: str) -> str:
    return ZONE_ALIASES.get(zone_code, zone_code)


def evaluate_animal_intrusion(db: Session, transition: ZoneTransition) -> Optional[dict]:
    object_type = transition.object_type.lower()
    if object_type not in ANIMAL_OBJECT_TYPES:
        return None

    policy = db.scalar(
        select(AnimalIntrusionPolicy)
        .where(AnimalIntrusionPolicy.object_type == object_type)
        .where(AnimalIntrusionPolicy.enabled.is_(True))
        .limit(1)
    )
    if not policy:
        return None

    to_zone = normalize_zone_code(transition.to_zone)
    allowed_zones = {normalize_zone_code(zone) for zone in policy.allowed_zones}
    restricted_zones = {normalize_zone_code(zone) for zone in policy.restricted_zones}

    violation_reason = None
    if to_zone in restricted_zones:
        violation_reason = "restricted_zone_entry"
    elif allowed_zones and to_zone not in allowed_zones:
        violation_reason = "outside_allowed_zone"

    if not violation_reason:
        return None

    camera = db.get(Camera, transition.camera_id) or db.get(Camera, DEFAULT_CAMERA_ID)
    to_zone_meta = _lookup_zone_metadata(db, to_zone)
    event_id = f"EVT-ANI-{uuid.uuid4().hex[:8].upper()}"
    snapshot_id = f"SNP-ANI-{uuid.uuid4().hex[:8].upper()}"
    alert_type = _violation_label(object_type, to_zone)[:120]

    event = Event(
        id=event_id,
        farm_id=camera.farm_id if camera else "FARM-001",
        camera_id=camera.id if camera else transition.camera_id,
        category="animal_intrusion",
        alert_type=alert_type,
        zone=to_zone,
        severity=policy.severity,
        status="new",
        handler="Chưa phân công",
        confidence=99,
        occurred_at=transition.cross_time,
    )
    snapshot = create_event_snapshot(
        event_id=event_id,
        snapshot_id=snapshot_id,
        storage_category="animal-intrusion",
        annotation=SnapshotAnnotation(
            object_label=object_type,
            zone_name=resolve_zone_display_name(db, to_zone),
            rule_name=f"Animal Intrusion Policy ({object_type})",
            timestamp=transition.cross_time,
            severity=policy.severity,
            track_id=transition.track_id,
            confidence=99,
        ),
    )

    db.add(event)
    db.add(snapshot)
    write_audit_log(
        db,
        user_id="SYSTEM",
        action="animal_intrusion_violation",
        resource_type="zone_transition",
        resource_id=transition.id,
        metadata={
            "policy_id": policy.id,
            "object_type": object_type,
            "violation_reason": violation_reason,
            "allowed_zones": sorted(allowed_zones),
            "restricted_zones": sorted(restricted_zones),
            "event_id": event_id,
            "snapshot_id": snapshot_id,
            "track_id": transition.track_id,
            "camera_id": transition.camera_id,
            "from_zone": transition.from_zone,
            "to_zone": to_zone,
            "zone_category": to_zone_meta.get("zone_category"),
            "biosecurity_level": to_zone_meta.get("biosecurity_level"),
            "risk_level": to_zone_meta.get("risk_level"),
        },
    )

    return {
        "type": "animal_intrusion",
        "policy_id": policy.id,
        "object_type": object_type,
        "severity": policy.severity,
        "violation_reason": violation_reason,
        "event_id": event_id,
        "snapshot_id": snapshot_id,
        "transition_id": transition.id,
        "track_id": transition.track_id,
        "camera_id": transition.camera_id,
        "from_zone": transition.from_zone,
        "to_zone": to_zone,
        "allowed_zones": sorted(allowed_zones),
        "restricted_zones": sorted(restricted_zones),
        "occurred_at": transition.cross_time,
        "notification": {
            "email": True,
            "telegram": policy.severity in {"critical", "high"},
            "zalo": policy.severity == "critical",
        },
    }


def _lookup_zone_metadata(db: Session, zone_code: str) -> dict:
    farm_zone = db.scalar(select(FarmZone).where(FarmZone.zone_code == zone_code).limit(1))
    if farm_zone:
        return {
            "zone_category": farm_zone.zone_category,
            "biosecurity_level": farm_zone.biosecurity_level,
            "risk_level": farm_zone.risk_level,
        }
    return {}
