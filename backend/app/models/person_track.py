from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PersonTrack(Base):
    __tablename__ = "person_tracks"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)
    track_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    zone_id: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    enter_time: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    exit_time: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
