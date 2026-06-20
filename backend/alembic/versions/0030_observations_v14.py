"""observations for evaluator foundation v1.4

Revision ID: 0030_observations_v14
Revises: 0029_event_rule_engine
Create Date: 2026-06-22 10:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0030_observations_v14"
down_revision: Optional[str] = "0029_event_rule_engine"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "observations",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("timestamp", sa.String(length=32), nullable=False),
        sa.Column("source", sa.String(length=20), nullable=False),
        sa.Column("frame_width", sa.Integer(), nullable=False),
        sa.Column("frame_height", sa.Integer(), nullable=False),
        sa.Column("objects", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_observations_camera_id"), "observations", ["camera_id"], unique=False)
    op.create_index(op.f("ix_observations_id"), "observations", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_observations_id"), table_name="observations")
    op.drop_index(op.f("ix_observations_camera_id"), table_name="observations")
    op.drop_table("observations")
