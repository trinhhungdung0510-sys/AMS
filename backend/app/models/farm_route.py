from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class FarmRoute(Base):
    __tablename__ = "farm_routes"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    layout_id: Mapped[str] = mapped_column(String(20), ForeignKey("farm_layouts.id"), nullable=False, index=True)
    route_type: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    points: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    labels: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    valid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
