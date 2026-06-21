from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Event
from app.services.system_settings_service import get_retention_days

logger = logging.getLogger(__name__)


def _cutoff_iso(days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()


def run_retention_cleanup(db: Session) -> dict[str, int]:
    retention_days = get_retention_days(db)
    cutoff = _cutoff_iso(retention_days)
    settings = get_settings()
    uploads_root = Path(settings.uploads_root)

    old_events = list(db.scalars(select(Event).where(Event.occurred_at < cutoff)))

    deleted_events = 0
    deleted_snapshots = 0

    if old_events:
        event_ids = [event.id for event in old_events]
        for event in old_events:
            snapshot_url = event.snapshot_url
            if not snapshot_url:
                continue
            relative = snapshot_url.lstrip("/")
            if relative.startswith("uploads/"):
                relative = relative[len("uploads/") :]
            file_path = uploads_root / relative
            if file_path.exists() and file_path.is_file():
                try:
                    file_path.unlink()
                    deleted_snapshots += 1
                except OSError:
                    logger.warning("Could not delete snapshot %s", file_path)

        db.execute(delete(Event).where(Event.id.in_(event_ids)))
        db.commit()
        deleted_events = len(event_ids)

    logger.info(
        "[Retention] days=%s cutoff=%s deleted_events=%s deleted_snapshots=%s",
        retention_days,
        cutoff,
        deleted_events,
        deleted_snapshots,
    )
    return {
        "retentionDays": retention_days,
        "deletedEvents": deleted_events,
        "deletedSnapshots": deleted_snapshots,
    }
