from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.models import Camera, Event
from app.services.demo_assets_service import snapshot_url_for_event_type
from app.services.evaluator_event_service import create_compliance_violation_event

DEMO_EVENT_TYPES = (
    COMPLIANCE_RULE_IDS["UNIFORM_VIOLATION"],
    COMPLIANCE_RULE_IDS["ZONE_INTRUSION"],
    COMPLIANCE_RULE_IDS["ANIMAL_INTRUSION"],
    COMPLIANCE_RULE_IDS["BIOSECURITY_PROCESS_VIOLATION"],
    COMPLIANCE_RULE_IDS["VEHICLE_INTRUSION"],
)

DEMO_ZONES = (
    "gestation_barn",
    "shower_room",
    "handwash_zone",
    "boot_disinfection_tray",
    "farm_gate",
)

DEMO_RULE_NAMES = {
    COMPLIANCE_RULE_IDS["UNIFORM_VIOLATION"]: "Sai đồng phục vùng",
    COMPLIANCE_RULE_IDS["ZONE_INTRUSION"]: "Xâm nhập vùng cấm",
    COMPLIANCE_RULE_IDS["ANIMAL_INTRUSION"]: "Động vật xâm nhập",
    COMPLIANCE_RULE_IDS["BIOSECURITY_PROCESS_VIOLATION"]: "Vi phạm quy trình an toàn sinh học",
    COMPLIANCE_RULE_IDS["VEHICLE_INTRUSION"]: "Xe xâm nhập / chưa sát trùng",
}


def _random_recent_timestamp(*, use_today: bool = False, max_hours: int = 72) -> str:
    now = datetime.now(timezone.utc)
    if use_today:
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        offset_minutes = random.randint(0, max(int((now - start).total_seconds() // 60), 1))
        moment = start + timedelta(minutes=offset_minutes)
    else:
        offset_minutes = random.randint(0, max_hours * 60)
        moment = now - timedelta(minutes=offset_minutes)
    return moment.isoformat()


def generate_demo_violations(
    db: Session,
    *,
    count: int = 12,
    publish: bool = False,
    use_today: bool = False,
    farm_id: str | None = None,
) -> list[Event]:
    query = select(Camera).where(Camera.is_active.is_(True))
    if farm_id:
        query = query.where(Camera.farm_id == farm_id)
    cameras = list(db.scalars(query.limit(20)))
    if not cameras:
        return []

    created: list[Event] = []
    for index in range(count):
        camera = random.choice(cameras)
        event_type = DEMO_EVENT_TYPES[index % len(DEMO_EVENT_TYPES)]
        zone_code = camera.zone or random.choice(DEMO_ZONES)
        track_id = random.randint(100, 999)
        score = round(random.uniform(0.55, 0.95), 2)

        event = create_compliance_violation_event(
            db,
            event_type=event_type,
            rule_id=event_type.lower(),
            rule_name=DEMO_RULE_NAMES[event_type],
            camera_id=camera.id,
            zone_id=zone_code,
            track_id=track_id,
            score=score,
            snapshot_path=snapshot_url_for_event_type(event_type),
            timestamp=_random_recent_timestamp(use_today=use_today),
            evidence={"source": "demo_generator", "demo_index": index + 1, "demoMode": True},
            publish=publish,
        )
        created.append(event)
    return created
