from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class NotificationRule(Base):
    __tablename__ = "notification_rules"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    alert_category: Mapped[str] = mapped_column(String(80), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    telegram: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    zalo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
