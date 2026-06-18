from sqlalchemy import Boolean, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class FarmMapLayer(Base):
    __tablename__ = "farm_map_layers"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    layout_id: Mapped[str] = mapped_column(String(20), ForeignKey("farm_layouts.id"), nullable=False, index=True)
    layer_key: Mapped[str] = mapped_column(String(30), nullable=False)
    visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    opacity: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
