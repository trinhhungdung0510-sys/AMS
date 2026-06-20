from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

OBJECT_CLASSES = {"PERSON", "ANIMAL", "VEHICLE"}
OBSERVATION_SOURCES = {"MOCK", "YOLO", "OPENVINO", "MANUAL"}


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    timestamp: Mapped[str] = mapped_column(String(32), nullable=False)
    source: Mapped[str] = mapped_column(String(20), nullable=False)
    frame_width: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_height: Mapped[int] = mapped_column(Integer, nullable=False)
    objects: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
