from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class AlertCategory(Base):
    __tablename__ = "alert_categories"

    code: Mapped[str] = mapped_column(String(80), primary_key=True, index=True)
    label: Mapped[str] = mapped_column(String(160), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
