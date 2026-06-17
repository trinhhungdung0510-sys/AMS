from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TemplateZoneDefinition(Base):
    __tablename__ = "template_zone_definitions"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    template_id: Mapped[str] = mapped_column(String(24), index=True, nullable=False)
    zone_code: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    zone_name: Mapped[str] = mapped_column(String(120), nullable=False)
    zone_category: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    biosecurity_level: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False)
    layout_x: Mapped[float] = mapped_column(Float, nullable=False)
    layout_y: Mapped[float] = mapped_column(Float, nullable=False)
    layout_w: Mapped[float] = mapped_column(Float, nullable=False)
    layout_h: Mapped[float] = mapped_column(Float, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
