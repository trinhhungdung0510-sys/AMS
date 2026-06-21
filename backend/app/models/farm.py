from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Farm(Base):
    __tablename__ = "farms"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    created_at: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    location: Mapped[str] = mapped_column(String(160), nullable=False)
    plan: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
