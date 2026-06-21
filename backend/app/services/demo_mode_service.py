from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.services.system_settings_service import get_system_settings


def is_demo_mode(db: Session | None = None) -> bool:
    if get_settings().demo_mode:
        return True
    if db is None:
        return False
    return bool(get_system_settings(db).get("demo_mode"))
