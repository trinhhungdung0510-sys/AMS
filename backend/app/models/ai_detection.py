from __future__ import annotations

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class AiDetection(Base):
    __tablename__ = "ai_detections"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    label: Mapped[str] = mapped_column(String(40), nullable=False)
    confidence: Mapped[float] = mapped_column(nullable=False)
    bbox: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
