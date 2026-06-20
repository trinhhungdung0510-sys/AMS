"""add zone reference dimensions and points format for v1.2

Revision ID: 0027_zone_reference_dims
Revises: 0026_camera_zones_v11
Create Date: 2026-06-21 10:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0027_zone_reference_dims"
down_revision: Optional[str] = "0026_camera_zones_v11"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.add_column("camera_zones", sa.Column("reference_width", sa.Integer(), nullable=True))
    op.add_column("camera_zones", sa.Column("reference_height", sa.Integer(), nullable=True))
    op.add_column(
        "camera_zones",
        sa.Column("points_format", sa.String(length=20), nullable=False, server_default="pixel"),
    )
    op.execute("UPDATE camera_zones SET points_format = 'pixel' WHERE points_format IS NULL")


def downgrade() -> None:
    op.drop_column("camera_zones", "points_format")
    op.drop_column("camera_zones", "reference_height")
    op.drop_column("camera_zones", "reference_width")
