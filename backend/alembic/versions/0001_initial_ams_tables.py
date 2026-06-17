"""initial ams tables

Revision ID: 0001_initial_ams_tables
Revises:
Create Date: 2026-06-17 16:20:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial_ams_tables"
down_revision: Optional[str] = None
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "cameras",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("zone", sa.String(length=80), nullable=False),
        sa.Column("ip_address", sa.String(length=45), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("resolution", sa.String(length=20), nullable=False),
        sa.Column("uptime", sa.Float(), nullable=False),
        sa.Column("fps", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ip_address"),
    )
    op.create_index(op.f("ix_cameras_id"), "cameras", ["id"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=160), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("role", sa.String(length=60), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "farm_zones",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("risk_level", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_farm_zones_id"), "farm_zones", ["id"], unique=False)

    op.create_table(
        "events",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("alert_type", sa.String(length=80), nullable=False),
        sa.Column("zone", sa.String(length=80), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("handler", sa.String(length=120), nullable=False),
        sa.Column("confidence", sa.Integer(), nullable=False),
        sa.Column("occurred_at", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["camera_id"], ["cameras.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_events_camera_id"), "events", ["camera_id"], unique=False)
    op.create_index(op.f("ix_events_id"), "events", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_events_id"), table_name="events")
    op.drop_index(op.f("ix_events_camera_id"), table_name="events")
    op.drop_table("events")
    op.drop_index(op.f("ix_farm_zones_id"), table_name="farm_zones")
    op.drop_table("farm_zones")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_cameras_id"), table_name="cameras")
    op.drop_table("cameras")
