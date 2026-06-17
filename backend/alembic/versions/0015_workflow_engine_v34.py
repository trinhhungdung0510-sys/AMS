"""workflow engine v34

Revision ID: 0015_workflow_engine_v34
Revises: 0014_animal_intrusion_engine_v33
Create Date: 2026-06-17 23:30:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0015_workflow_engine_v34"
down_revision: Optional[str] = "0014_animal_intrusion_engine_v33"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "workflows",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("object_type", sa.String(length=40), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_workflows_id"), "workflows", ["id"], unique=False)
    op.create_index(op.f("ix_workflows_object_type"), "workflows", ["object_type"], unique=False)

    op.create_table(
        "workflow_steps",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("workflow_id", sa.String(length=24), nullable=False),
        sa.Column("step_order", sa.Integer(), nullable=False),
        sa.Column("step_name", sa.String(length=120), nullable=False),
        sa.Column("zone_code", sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_workflow_steps_id"), "workflow_steps", ["id"], unique=False)
    op.create_index(op.f("ix_workflow_steps_workflow_id"), "workflow_steps", ["workflow_id"], unique=False)
    op.create_index(op.f("ix_workflow_steps_step_order"), "workflow_steps", ["step_order"], unique=False)
    op.create_index(op.f("ix_workflow_steps_zone_code"), "workflow_steps", ["zone_code"], unique=False)

    op.create_table(
        "track_workflow_progress",
        sa.Column("id", sa.String(length=48), nullable=False),
        sa.Column("track_id", sa.Integer(), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("workflow_id", sa.String(length=24), nullable=False),
        sa.Column("completed_step_order", sa.Integer(), nullable=False),
        sa.Column("last_zone", sa.String(length=40), nullable=False),
        sa.Column("updated_at", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_track_workflow_progress_id"), "track_workflow_progress", ["id"], unique=False)
    op.create_index(op.f("ix_track_workflow_progress_track_id"), "track_workflow_progress", ["track_id"], unique=False)
    op.create_index(op.f("ix_track_workflow_progress_camera_id"), "track_workflow_progress", ["camera_id"], unique=False)
    op.create_index(
        op.f("ix_track_workflow_progress_workflow_id"),
        "track_workflow_progress",
        ["workflow_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_track_workflow_progress_workflow_id"), table_name="track_workflow_progress")
    op.drop_index(op.f("ix_track_workflow_progress_camera_id"), table_name="track_workflow_progress")
    op.drop_index(op.f("ix_track_workflow_progress_track_id"), table_name="track_workflow_progress")
    op.drop_index(op.f("ix_track_workflow_progress_id"), table_name="track_workflow_progress")
    op.drop_table("track_workflow_progress")

    op.drop_index(op.f("ix_workflow_steps_zone_code"), table_name="workflow_steps")
    op.drop_index(op.f("ix_workflow_steps_step_order"), table_name="workflow_steps")
    op.drop_index(op.f("ix_workflow_steps_workflow_id"), table_name="workflow_steps")
    op.drop_index(op.f("ix_workflow_steps_id"), table_name="workflow_steps")
    op.drop_table("workflow_steps")

    op.drop_index(op.f("ix_workflows_object_type"), table_name="workflows")
    op.drop_index(op.f("ix_workflows_id"), table_name="workflows")
    op.drop_table("workflows")
