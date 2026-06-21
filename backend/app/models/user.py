from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.roles import DEFAULT_FARM_ID
from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(60), nullable=False)
    farm_id: Mapped[str] = mapped_column(String(20), default=DEFAULT_FARM_ID, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
