from __future__ import annotations

from typing import Optional

from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.roles import DEFAULT_FARM_ID
from app.database.base import Base

POINTS_FORMAT_PIXEL = "pixel"
POINTS_FORMAT_NORMALIZED = "normalized"


class CameraZone(Base):
    """Vùng giám sát trên ảnh camera. v1.2 lưu points chuẩn hóa (0–1) + reference dimensions."""

    __tablename__ = "camera_zones"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    farm_id: Mapped[str] = mapped_column(String(20), default=DEFAULT_FARM_ID, index=True, nullable=False)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    parent_zone_id: Mapped[Optional[str]] = mapped_column(String(24), index=True, nullable=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    zone_type: Mapped[str] = mapped_column(String(40), nullable=False, default="monitoring")
    points: Mapped[list[dict]] = mapped_column(JSON, nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False, default="#ff0000")
    reference_width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reference_height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    points_format: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=POINTS_FORMAT_PIXEL,
    )
    required_uniform_id: Mapped[Optional[str]] = mapped_column(String(24), index=True, nullable=True)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(32), nullable=False)
