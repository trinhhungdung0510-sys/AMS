"""camera editor zones v1.0 with normalized coordinates

Revision ID: 0024_camera_editor_zones
Revises: 0023_camera_ip_upgrade
Create Date: 2026-06-20 12:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0024_camera_editor_zones"
down_revision: Optional[str] = "0023_camera_ip_upgrade"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "camera_editor_zones",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("zone_type", sa.String(length=40), nullable=False),
        sa.Column("color", sa.String(length=20), nullable=False),
        sa.Column("points", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_camera_editor_zones_camera_id"), "camera_editor_zones", ["camera_id"], unique=False)
    op.create_index(op.f("ix_camera_editor_zones_id"), "camera_editor_zones", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_camera_editor_zones_id"), table_name="camera_editor_zones")
    op.drop_index(op.f("ix_camera_editor_zones_camera_id"), table_name="camera_editor_zones")
    op.drop_table("camera_editor_zones")
