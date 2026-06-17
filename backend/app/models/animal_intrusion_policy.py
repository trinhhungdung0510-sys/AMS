from sqlalchemy import Boolean, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class AnimalIntrusionPolicy(Base):
    __tablename__ = "animal_intrusion_policies"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    object_type: Mapped[str] = mapped_column(String(40), unique=True, index=True, nullable=False)
    allowed_zones: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    restricted_zones: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
