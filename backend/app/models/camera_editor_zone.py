from __future__ import annotations

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CameraEditorZone(Base):
    __tablename__ = "camera_editor_zones"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    zone_type: Mapped[str] = mapped_column(String(40), nullable=False, default="restricted")
    color: Mapped[str] = mapped_column(String(20), nullable=False, default="#ff0000")
    points: Mapped[list[dict]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
