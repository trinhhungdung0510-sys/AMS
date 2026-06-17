from sqlalchemy import Boolean, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ZonePolygon(Base):
    __tablename__ = "zone_polygons"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    farm_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    zone_name: Mapped[str] = mapped_column(String(120), nullable=False)
    zone_type: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    biosecurity_level: Mapped[str] = mapped_column(String(20), index=True, nullable=False, default="yellow")
    color: Mapped[str] = mapped_column(String(20), nullable=False)
    polygon_points: Mapped[list[list[float]]] = mapped_column(JSON, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
