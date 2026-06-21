from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.models import Camera, Event
from app.services.vi_localization import resolve_camera_name


def browse_evidence(
    db: Session,
    *,
    farm_id: str | None = None,
    camera_id: str | None = None,
    date_prefix: str | None = None,
    rule_type: str | None = None,
    page: int = 1,
    limit: int = 50,
) -> tuple[list[dict], int]:
    query = select(Event).where(Event.snapshot_url.isnot(None)).where(Event.snapshot_url != "")
    query = query.where(Event.category == "compliance_violation")

    if farm_id:
        query = query.where(Event.farm_id == farm_id)
    if camera_id:
        query = query.where(Event.camera_id == camera_id)
    if date_prefix:
        query = query.where(Event.occurred_at.startswith(date_prefix))
    if rule_type:
        if rule_type in COMPLIANCE_RULE_IDS.values():
            query = query.where(Event.event_type == rule_type)
        else:
            query = query.where(Event.event_type == rule_type)

    rows = list(db.scalars(query.order_by(Event.occurred_at.desc(), Event.id)))
    total = len(rows)
    offset = max(page - 1, 0) * limit
    page_rows = rows[offset : offset + limit]

    items = []
    for event in page_rows:
        metadata = event.event_metadata or {}
        items.append(
            {
                "id": event.id,
                "farmId": event.farm_id,
                "cameraId": event.camera_id,
                "cameraName": resolve_camera_name(db, event.camera_id),
                "ruleType": event.event_type,
                "ruleName": metadata.get("rule_name") or event.alert_type,
                "snapshotUrl": event.snapshot_url,
                "score": event.confidence_score,
                "occurredAt": event.occurred_at,
                "zone": event.zone,
            }
        )
    return items, total
