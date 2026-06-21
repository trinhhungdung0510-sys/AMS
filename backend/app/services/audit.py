from typing import Optional

from sqlalchemy.orm import Session

from app.models import AuditLog


def write_audit_log(
    db: Session,
    *,
    user_id: str,
    action: str,
    resource_type: str,
    resource_id: str,
    metadata: Optional[dict] = None,
    farm_id: Optional[str] = None,
) -> AuditLog:
    import json
    import uuid
    from datetime import datetime, timezone

    log = AuditLog(
        id=f"AUD-{uuid.uuid4().hex[:12].upper()}",
        farm_id=farm_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        metadata_json=json.dumps(metadata or {}, ensure_ascii=False),
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    db.add(log)
    return log
