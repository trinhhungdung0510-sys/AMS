from typing import Optional

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class AITask(Base):
    __tablename__ = "ai_tasks"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    result: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
    processed_at: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
