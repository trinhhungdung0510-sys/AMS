"""upgrade cameras table for real IP camera fields

Revision ID: 0023_camera_ip_upgrade
Revises: 0022_zone_designer_opacity
Create Date: 2026-06-19 10:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0023_camera_ip_upgrade"
down_revision: Optional[str] = "0022_zone_designer_opacity"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.alter_column("cameras", "ip_address", new_column_name="ip")

    op.add_column("cameras", sa.Column("manufacturer", sa.String(length=120), nullable=True))
    op.add_column("cameras", sa.Column("port", sa.Integer(), nullable=False, server_default="554"))
    op.add_column("cameras", sa.Column("username", sa.String(length=120), nullable=False, server_default="admin"))
    op.add_column("cameras", sa.Column("password", sa.String(length=255), nullable=False, server_default="admin123"))
    op.add_column("cameras", sa.Column("rtsp_url", sa.String(length=500), nullable=True))
    op.add_column("cameras", sa.Column("last_seen", sa.String(length=32), nullable=True))
    op.add_column(
        "cameras",
        sa.Column("created_at", sa.String(length=32), nullable=False, server_default="2026-01-01T00:00:00+00:00"),
    )


def downgrade() -> None:
    op.drop_column("cameras", "created_at")
    op.drop_column("cameras", "last_seen")
    op.drop_column("cameras", "rtsp_url")
    op.drop_column("cameras", "password")
    op.drop_column("cameras", "username")
    op.drop_column("cameras", "port")
    op.drop_column("cameras", "manufacturer")
    op.alter_column("cameras", "ip", new_column_name="ip_address")
