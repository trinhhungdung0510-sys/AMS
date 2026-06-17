from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    visitor_name: Mapped[str] = mapped_column(String(120), nullable=False)
    company: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    vehicle_plate: Mapped[str] = mapped_column(String(20), index=True, nullable=False, default="")
    visit_purpose: Mapped[str] = mapped_column(String(255), nullable=False)
    arrival_time: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    departure_time: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    approved_by: Mapped[str] = mapped_column(String(120), nullable=False)
