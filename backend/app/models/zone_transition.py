from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ZoneTransition(Base):
    __tablename__ = "zone_transitions"

    id: Mapped[str] = mapped_column(String(28), primary_key=True, index=True)
    track_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    object_type: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    from_zone: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    to_zone: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    cross_time: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    timestamp: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    atsh_rule_code: Mapped[Optional[str]] = mapped_column(String(80), index=True, nullable=True)
    atsh_severity: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
