from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CameraStream(Base):
    __tablename__ = "camera_streams"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(ForeignKey("cameras.id"), index=True, nullable=False)
    rtsp_url: Mapped[str] = mapped_column(String(255), nullable=False)
    fps: Mapped[int] = mapped_column(Integer, nullable=False)
    resolution: Mapped[str] = mapped_column(String(20), nullable=False)
    stream_status: Mapped[str] = mapped_column(String(20), nullable=False)
