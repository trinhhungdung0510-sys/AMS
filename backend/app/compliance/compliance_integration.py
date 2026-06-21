from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.compliance.compliance_engine import get_compliance_engine
from app.compliance.types import ComplianceContext
from app.models import CameraZone


def run_compliance_after_person_enter(
    db: Session,
    *,
    hit: dict[str, Any],
    track: dict[str, Any],
    observation: dict[str, Any],
    obj: dict[str, Any],
) -> None:
    zone = db.get(CameraZone, hit.get("zoneId") or hit.get("zone_id"))
    timestamp = observation.get("timestamp") or observation.get("created_at") or ""

    context = ComplianceContext(
        db=db,
        camera_id=track["cameraId"],
        zone_id=hit.get("zoneId") or hit.get("zone_id") or "",
        track_id=track.get("trackId"),
        timestamp=timestamp,
        observation=observation,
        metadata={
            "trigger_event": "PERSON_ENTER",
            "zone_name": zone.name if zone else hit.get("zoneId"),
            "bbox": obj.get("bbox"),
            "attributes": obj.get("attributes") or {},
            "person_snapshot": obj.get("personSnapshot") or obj.get("person_snapshot"),
            "snapshot_path": obj.get("snapshotPath") or obj.get("snapshot_path"),
        },
    )

    get_compliance_engine().evaluate(context)
