import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AITask, AlertCategory, Camera, Event
from app.services.audit import write_audit_log
from app.services.snapshot_generator import SnapshotAnnotation, create_event_snapshot, resolve_zone_display_name


def process_ai_task(db: Session, task: AITask) -> dict:
    camera = db.scalar(select(Camera).where(Camera.id == task.camera_id))
    category = db.scalar(select(AlertCategory).where(AlertCategory.code == task.category))

    if not camera or not category:
        task.status = "failed"
        task.result = json.dumps({"error": "camera_or_category_not_found"}, ensure_ascii=False)
        task.processed_at = datetime.now(timezone.utc).isoformat()
        db.add(task)
        return {"type": "task_failed", "task_id": task.id}

    now = datetime.now(timezone.utc)
    event_id = f"EVT-RT-{uuid.uuid4().hex[:8].upper()}"
    snapshot_id = f"SNP-RT-{uuid.uuid4().hex[:8].upper()}"
    confidence = 88 + (int(uuid.uuid4().hex[:2], 16) % 12)

    event = Event(
        id=event_id,
        farm_id=camera.farm_id,
        camera_id=camera.id,
        category=category.code,
        alert_type=category.label,
        zone=camera.zone,
        severity=category.severity,
        status="new",
        handler="Chưa phân công",
        confidence=confidence,
        occurred_at=now.isoformat(),
    )
    snapshot = create_event_snapshot(
        event_id=event_id,
        snapshot_id=snapshot_id,
        storage_category="runtime",
        annotation=SnapshotAnnotation(
            object_label=category.label,
            zone_name=resolve_zone_display_name(db, camera.zone),
            rule_name=category.label,
            timestamp=now.isoformat(),
            severity=category.severity,
            confidence=confidence,
        ),
    )

    task.status = "completed"
    task.processed_at = now.isoformat()
    task.result = json.dumps(
        {
            "event_id": event_id,
            "snapshot_id": snapshot_id,
            "notification": "triggered",
            "confidence": confidence,
        },
        ensure_ascii=False,
    )

    db.add(event)
    db.add(snapshot)
    db.add(task)
    write_audit_log(
        db,
        user_id="SYSTEM",
        action="ai_task_completed",
        resource_type="ai_task",
        resource_id=task.id,
        metadata={"event_id": event_id, "snapshot_id": snapshot_id},
    )

    return {
        "type": "alert",
        "task_id": task.id,
        "event_id": event_id,
        "snapshot_id": snapshot_id,
        "camera_id": camera.id,
        "camera_name": camera.name,
        "zone": camera.zone,
        "category": category.code,
        "alert_type": category.label,
        "severity": category.severity,
        "confidence": confidence,
        "occurred_at": event.occurred_at,
        "notification": {"email": True, "telegram": category.severity in {"danger", "critical"}},
    }
