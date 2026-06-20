from __future__ import annotations

from typing import Optional

from typing import Any

from sqlalchemy import Boolean, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

RULE_TYPES = {
    "PERSON_ENTER",
    "PERSON_DWELL",
    "PERSON_COUNT",
    "ANIMAL_ENTER",
    "PPE_REQUIRED",
    "HANDWASH_REQUIRED",
    "DISINFECTION_REQUIRED",
    "CROSS_LINE",
}

RULE_SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


class ZoneRule(Base):
    __tablename__ = "zone_rules"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    zone_id: Mapped[str] = mapped_column(String(24), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    rule_type: Mapped[str] = mapped_column(String(40), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="MEDIUM")
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    cooldown_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(32), nullable=False)
