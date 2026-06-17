from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class NotificationGateway(Base):
    __tablename__ = "notification_gateways"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    farm_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    gateway_type: Mapped[str] = mapped_column(String(30), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
