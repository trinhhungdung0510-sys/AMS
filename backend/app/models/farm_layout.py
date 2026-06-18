from sqlalchemy import Boolean, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class FarmLayout(Base):
    __tablename__ = "farm_layouts"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    farm_id: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False, default="")
    center_lat: Mapped[float] = mapped_column(Float, nullable=False)
    center_lng: Mapped[float] = mapped_column(Float, nullable=False)
    zoom: Mapped[int] = mapped_column(nullable=False, default=17)
    base_layer: Mapped[str] = mapped_column(String(20), nullable=False, default="satellite")
    is_template: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
