from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CameraHealth(Base):
    __tablename__ = "camera_health"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    farm_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    fps: Mapped[int] = mapped_column(Integer, nullable=False)
    bitrate: Mapped[float] = mapped_column(Float, nullable=False)
    last_seen: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
