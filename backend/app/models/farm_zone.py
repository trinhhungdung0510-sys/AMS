from typing import Optional

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class FarmZone(Base):
    __tablename__ = "farm_zones"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    farm_id: Mapped[Optional[str]] = mapped_column(String(20), index=True, nullable=True)
    template_id: Mapped[Optional[str]] = mapped_column(String(24), index=True, nullable=True)
    template_zone_id: Mapped[Optional[str]] = mapped_column(String(24), index=True, nullable=True)
    zone_code: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    zone_category: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    biosecurity_level: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), default="online", nullable=False)
    layout_x: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    layout_y: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    layout_w: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    layout_h: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
