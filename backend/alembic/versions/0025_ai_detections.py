"""ai detections v1.0 with normalized bbox

Revision ID: 0025_ai_detections
Revises: 0024_camera_editor_zones
Create Date: 2026-06-20 14:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0025_ai_detections"
down_revision: Optional[str] = "0024_camera_editor_zones"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "ai_detections",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("label", sa.String(length=40), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("bbox", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_detections_camera_id"), "ai_detections", ["camera_id"], unique=False)
    op.create_index(op.f("ix_ai_detections_id"), "ai_detections", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_ai_detections_id"), table_name="ai_detections")
    op.drop_index(op.f("ix_ai_detections_camera_id"), table_name="ai_detections")
    op.drop_table("ai_detections")
