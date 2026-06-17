from typing import Optional

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ObjectTrack(Base):
    __tablename__ = "object_tracks"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)
    track_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    object_type: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    current_zone: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    previous_zone: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    employee_id: Mapped[Optional[str]] = mapped_column(String(24), index=True, nullable=True)
    enter_time: Mapped[str] = mapped_column(String(32), nullable=False)
    leave_time: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    last_seen: Mapped[str] = mapped_column(String(32), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
