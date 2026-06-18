import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.biosecurity_ai_v40 import AI_CATEGORY_TO_ATSH_RULE
from app.models import AITask, AlertCategory, BiosecurityRule, Camera
from app.services.atsh_biosecurity_engine import create_atsh_violation_event
from app.services.audit import write_audit_log
from app.services.snapshot_generator import resolve_zone_display_name


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
    confidence = 88 + (int(uuid.uuid4().hex[:2], 16) % 12)
    rule_code = AI_CATEGORY_TO_ATSH_RULE.get(category.code, "FORBIDDEN_ZONE_INTRUSION")
    rule = db.scalar(
        select(BiosecurityRule)
        .where(BiosecurityRule.rule_code == rule_code)
        .where(BiosecurityRule.enabled.is_(True))
        .limit(1)
    )

    if rule:
        payload = create_atsh_violation_event(
            db,
            rule=rule,
            transition=None,
            camera_id=camera.id,
            zone_code=camera.zone,
            object_type=category.code,
            occurred_at=now.isoformat(),
            confidence=confidence,
        )
        event_id = payload["event_id"]
        snapshot_id = payload["snapshot_id"]
        alert_type = payload["ten_vi_pham"]
        severity = payload["severity"]
    else:
        from app.models import Event
        from app.services.snapshot_generator import SnapshotAnnotation, create_event_snapshot

        event_id = f"EVT-RT-{uuid.uuid4().hex[:8].upper()}"
        snapshot_id = f"SNP-RT-{uuid.uuid4().hex[:8].upper()}"
        alert_type = category.label
        severity = category.severity
        event = Event(
            id=event_id,
            farm_id=camera.farm_id,
            camera_id=camera.id,
            category="atsh_violation",
            alert_type=f"Vi phạm ATSH: {category.label}"[:120],
            zone=camera.zone,
            severity=severity,
            status="new",
            handler="Chưa phân công",
            confidence=confidence,
            occurred_at=now.isoformat(),
            violation_code=rule_code,
        )
        snapshot = create_event_snapshot(
            event_id=event_id,
            snapshot_id=snapshot_id,
            storage_category="biosecurity",
            annotation=SnapshotAnnotation(
                object_label=category.label,
                zone_name=resolve_zone_display_name(db, camera.zone),
                rule_name=category.label,
                timestamp=now.isoformat(),
                severity=severity,
                confidence=confidence,
            ),
        )
        db.add(event)
        db.add(snapshot)
        payload = {"event_id": event_id, "snapshot_id": snapshot_id, "severity": severity}

    task.status = "completed"
    task.processed_at = now.isoformat()
    task.result = json.dumps(
        {
            "event_id": event_id,
            "snapshot_id": snapshot_id,
            "notification": "triggered",
            "confidence": confidence,
            "atsh_rule_code": rule_code,
        },
        ensure_ascii=False,
    )

    db.add(task)
    write_audit_log(
        db,
        user_id="SYSTEM",
        action="ai_task_completed",
        resource_type="ai_task",
        resource_id=task.id,
        metadata={"event_id": event_id, "snapshot_id": snapshot_id, "atsh_rule_code": rule_code},
    )

    return {
        "type": "atsh_violation",
        "task_id": task.id,
        "event_id": event_id,
        "snapshot_id": snapshot_id,
        "camera_id": camera.id,
        "camera_name": camera.name,
        "zone": camera.zone,
        "category": category.code,
        "alert_type": alert_type,
        "rule_code": rule_code,
        "severity": payload.get("severity", category.severity),
        "confidence": confidence,
        "occurred_at": now.isoformat(),
        "notification": {"email": True, "telegram": payload.get("severity") == "CRITICAL"},
    }
