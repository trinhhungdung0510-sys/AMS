from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class EventSnapshot(Base):
    __tablename__ = "event_snapshots"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    event_id: Mapped[str] = mapped_column(ForeignKey("events.id"), index=True, nullable=False)
    image_path: Mapped[str] = mapped_column(String(255), nullable=False)
    thumbnail_path: Mapped[str] = mapped_column(String(255), nullable=False)
