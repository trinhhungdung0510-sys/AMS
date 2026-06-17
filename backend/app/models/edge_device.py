from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class EdgeDevice(Base):
    __tablename__ = "edge_devices"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    farm_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    device_name: Mapped[str] = mapped_column(String(120), nullable=False)
    device_type: Mapped[str] = mapped_column(String(60), nullable=False)
    serial_number: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    assigned_cameras: Mapped[int] = mapped_column(Integer, nullable=False)
