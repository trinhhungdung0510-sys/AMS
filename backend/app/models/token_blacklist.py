from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    jti: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(20), nullable=False)
    expires_at: Mapped[int] = mapped_column(Integer, nullable=False)
