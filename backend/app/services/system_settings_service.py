from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import SystemSetting

SETTING_KEYS = (
    "compliance_threshold",
    "workflow_timeout",
    "demo_mode",
    "retention_days",
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _defaults() -> dict[str, Any]:
    settings = get_settings()
    return {
        "compliance_threshold": settings.compliance_uniform_threshold,
        "workflow_timeout": settings.workflow_timeout_seconds,
        "demo_mode": settings.demo_mode,
        "retention_days": settings.retention_days,
    }


def get_system_settings(db: Session) -> dict[str, Any]:
    values = _defaults()
    rows = list(db.scalars(select(SystemSetting)))
    for row in rows:
        try:
            values[row.key] = json.loads(row.value_json)
        except json.JSONDecodeError:
            continue
    return values


def save_system_settings(
    db: Session,
    payload: dict[str, Any],
    *,
    updated_by: str | None = None,
) -> dict[str, Any]:
    now = utc_now_iso()
    for key in SETTING_KEYS:
        if key not in payload:
            continue
        row = db.get(SystemSetting, key)
        if row is None:
            row = SystemSetting(key=key, value_json="{}", updated_at=now, updated_by=updated_by)
        row.value_json = json.dumps(payload[key], ensure_ascii=False)
        row.updated_at = now
        row.updated_by = updated_by
        db.add(row)
    db.commit()
    return get_system_settings(db)


def get_retention_days(db: Session) -> int:
    value = get_system_settings(db).get("retention_days", 90)
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return 90
