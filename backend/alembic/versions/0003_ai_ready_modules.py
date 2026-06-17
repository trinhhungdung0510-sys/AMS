"""ai ready modules

Revision ID: 0003_ai_ready_modules
Revises: 0002_auth_categories_dashboard
Create Date: 2026-06-17 17:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003_ai_ready_modules"
down_revision: Optional[str] = "0002_auth_categories_dashboard"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "ai_models",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("model_name", sa.String(length=120), nullable=False),
        sa.Column("model_type", sa.String(length=80), nullable=False),
        sa.Column("version", sa.String(length=40), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_models_id"), "ai_models", ["id"], unique=False)

    op.create_table(
        "camera_streams",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("rtsp_url", sa.String(length=255), nullable=False),
        sa.Column("fps", sa.Integer(), nullable=False),
        sa.Column("resolution", sa.String(length=20), nullable=False),
        sa.Column("stream_status", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["camera_id"], ["cameras.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_camera_streams_camera_id"), "camera_streams", ["camera_id"], unique=False)
    op.create_index(op.f("ix_camera_streams_id"), "camera_streams", ["id"], unique=False)

    op.create_table(
        "event_snapshots",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("event_id", sa.String(length=20), nullable=False),
        sa.Column("image_path", sa.String(length=255), nullable=False),
        sa.Column("thumbnail_path", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_event_snapshots_event_id"), "event_snapshots", ["event_id"], unique=False)
    op.create_index(op.f("ix_event_snapshots_id"), "event_snapshots", ["id"], unique=False)

    op.create_table(
        "farm_map_objects",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("object_type", sa.String(length=40), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("zone", sa.String(length=80), nullable=False),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_farm_map_objects_id"), "farm_map_objects", ["id"], unique=False)

    op.create_table(
        "notification_rules",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("alert_category", sa.String(length=80), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("email", sa.Boolean(), nullable=False),
        sa.Column("telegram", sa.Boolean(), nullable=False),
        sa.Column("zalo", sa.Boolean(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_notification_rules_id"), "notification_rules", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_notification_rules_id"), table_name="notification_rules")
    op.drop_table("notification_rules")
    op.drop_index(op.f("ix_farm_map_objects_id"), table_name="farm_map_objects")
    op.drop_table("farm_map_objects")
    op.drop_index(op.f("ix_event_snapshots_id"), table_name="event_snapshots")
    op.drop_index(op.f("ix_event_snapshots_event_id"), table_name="event_snapshots")
    op.drop_table("event_snapshots")
    op.drop_index(op.f("ix_camera_streams_id"), table_name="camera_streams")
    op.drop_index(op.f("ix_camera_streams_camera_id"), table_name="camera_streams")
    op.drop_table("camera_streams")
    op.drop_index(op.f("ix_ai_models_id"), table_name="ai_models")
    op.drop_table("ai_models")
