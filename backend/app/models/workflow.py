from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.roles import DEFAULT_FARM_ID
from app.database.base import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    farm_id: Mapped[str] = mapped_column(String(20), default=DEFAULT_FARM_ID, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    object_type: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    workflow_id: Mapped[str] = mapped_column(String(24), index=True, nullable=False)
    step_order: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    step_name: Mapped[str] = mapped_column(String(120), nullable=False)
    zone_code: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class TrackWorkflowProgress(Base):
    __tablename__ = "track_workflow_progress"

    id: Mapped[str] = mapped_column(String(48), primary_key=True, index=True)
    track_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    camera_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    workflow_id: Mapped[str] = mapped_column(String(24), index=True, nullable=False)
    completed_step_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_zone: Mapped[str] = mapped_column(String(40), nullable=False, default="")
    updated_at: Mapped[str] = mapped_column(String(32), nullable=False)
