from __future__ import annotations

from typing import Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class NotificationDispatch(Base):
    """One row per violation event — prevents duplicate outbound notifications."""

    __tablename__ = "notification_dispatches"

    event_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    farm_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    dispatched_at: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
