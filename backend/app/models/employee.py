from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    employee_code: Mapped[str] = mapped_column(String(40), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    department: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    assigned_zone: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    uniform_color: Mapped[str] = mapped_column(String(40), nullable=False)
    face_image: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
