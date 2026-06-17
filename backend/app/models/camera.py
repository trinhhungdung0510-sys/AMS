from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    farm_id: Mapped[str] = mapped_column(String(20), default="FARM-001", index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    zone: Mapped[str] = mapped_column(String(80), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="online", nullable=False)
    resolution: Mapped[str] = mapped_column(String(20), default="1080p", nullable=False)
    uptime: Mapped[float] = mapped_column(Float, default=99.0, nullable=False)
    fps: Mapped[int] = mapped_column(Integer, default=25, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
