"""camera zones v1.1 with hierarchy and pixel coordinates

Revision ID: 0026_camera_zones_v11
Revises: 0025_ai_detections
Create Date: 2026-06-20 16:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0026_camera_zones_v11"
down_revision: Optional[str] = "0025_ai_detections"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "camera_zones",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("parent_zone_id", sa.String(length=24), nullable=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("zone_type", sa.String(length=40), nullable=False),
        sa.Column("points", sa.JSON(), nullable=False),
        sa.Column("color", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.Column("updated_at", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_camera_zones_camera_id"), "camera_zones", ["camera_id"], unique=False)
    op.create_index(op.f("ix_camera_zones_id"), "camera_zones", ["id"], unique=False)
    op.create_index(op.f("ix_camera_zones_parent_zone_id"), "camera_zones", ["parent_zone_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_camera_zones_parent_zone_id"), table_name="camera_zones")
    op.drop_index(op.f("ix_camera_zones_id"), table_name="camera_zones")
    op.drop_index(op.f("ix_camera_zones_camera_id"), table_name="camera_zones")
    op.drop_table("camera_zones")
