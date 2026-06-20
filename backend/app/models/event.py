from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

EVENT_STATUSES = {"OPEN", "ACKNOWLEDGED", "RESOLVED"}


class Event(Base):
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    farm_id: Mapped[str] = mapped_column(String(20), default="FARM-001", index=True, nullable=False)
    camera_id: Mapped[str] = mapped_column(ForeignKey("cameras.id"), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(80), default="improper_clothing", nullable=False)
    alert_type: Mapped[str] = mapped_column(String(80), nullable=False)
    zone: Mapped[str] = mapped_column(String(80), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    handler: Mapped[str] = mapped_column(String(120), nullable=False)
    confidence: Mapped[int] = mapped_column(Integer, nullable=False)
    occurred_at: Mapped[str] = mapped_column(String(32), nullable=False)
    violation_code: Mapped[Optional[str]] = mapped_column(String(40), index=True, nullable=True)

    # Rule Engine v1.3
    zone_id: Mapped[Optional[str]] = mapped_column(String(24), index=True, nullable=True)
    rule_id: Mapped[Optional[str]] = mapped_column(String(24), index=True, nullable=True)
    event_type: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    confidence_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    snapshot_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    started_at: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    ended_at: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    event_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    record_created_at: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
