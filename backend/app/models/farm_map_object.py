from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class FarmMapObject(Base):
    __tablename__ = "farm_map_objects"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    object_type: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    zone: Mapped[str] = mapped_column(String(80), nullable=False)
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
