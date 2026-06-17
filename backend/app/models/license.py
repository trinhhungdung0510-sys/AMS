from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class License(Base):
    __tablename__ = "licenses"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    farm_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    plan: Mapped[str] = mapped_column(String(40), nullable=False)
    max_cameras: Mapped[int] = mapped_column(Integer, nullable=False)
    max_ai_models: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[str] = mapped_column(String(20), nullable=False)
    end_date: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
