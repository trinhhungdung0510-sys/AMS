from typing import Optional

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class BiosecurityRule(Base):
    __tablename__ = "biosecurity_rules"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    rule_code: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    rule_name_vi: Mapped[str] = mapped_column(String(160), nullable=False)
    rule_name_en: Mapped[str] = mapped_column(String(160), nullable=False)
    category: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
    object_type: Mapped[Optional[str]] = mapped_column(String(40), index=True, nullable=True)
    from_zone: Mapped[Optional[str]] = mapped_column(String(40), index=True, nullable=True)
    to_zone: Mapped[Optional[str]] = mapped_column(String(40), index=True, nullable=True)
    required_zone: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    rule_type: Mapped[Optional[str]] = mapped_column(String(40), index=True, nullable=True)
    evaluation_mode: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
