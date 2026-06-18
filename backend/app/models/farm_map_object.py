from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class FarmMapObject(Base):
    __tablename__ = "farm_map_objects"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    layout_id: Mapped[str | None] = mapped_column(
        String(20), ForeignKey("farm_map_layouts.id"), nullable=True, index=True
    )
    object_type: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    zone: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
    width: Mapped[float] = mapped_column(Float, nullable=False, default=0.0003)
    height: Mapped[float] = mapped_column(Float, nullable=False, default=0.0003)
    rotation: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    atsh_zone_type: Mapped[str] = mapped_column(String(30), nullable=False, default="buffer")
    atsh_level: Mapped[str] = mapped_column(String(20), nullable=False, default="green")
    linked_camera_id: Mapped[str | None] = mapped_column(String(20), nullable=True)
    linked_zone_id: Mapped[str | None] = mapped_column(String(20), nullable=True)
    camera_direction: Mapped[float | None] = mapped_column(Float, nullable=True)
    camera_fov: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
