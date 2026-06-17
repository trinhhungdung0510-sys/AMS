"""enterprise multi farm

Revision ID: 0005_enterprise_multi_farm
Revises: 0004_ai_runtime
Create Date: 2026-06-17 17:15:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0005_enterprise_multi_farm"
down_revision: Optional[str] = "0004_ai_runtime"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "farms",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("location", sa.String(length=160), nullable=False),
        sa.Column("plan", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_farms_id"), "farms", ["id"], unique=False)

    op.add_column("cameras", sa.Column("farm_id", sa.String(length=20), server_default="FARM-001", nullable=False))
    op.create_index(op.f("ix_cameras_farm_id"), "cameras", ["farm_id"], unique=False)
    op.alter_column("cameras", "farm_id", server_default=None)

    op.add_column("events", sa.Column("farm_id", sa.String(length=20), server_default="FARM-001", nullable=False))
    op.create_index(op.f("ix_events_farm_id"), "events", ["farm_id"], unique=False)
    op.alter_column("events", "farm_id", server_default=None)

    op.create_table(
        "camera_health",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("farm_id", sa.String(length=20), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("fps", sa.Integer(), nullable=False),
        sa.Column("bitrate", sa.Float(), nullable=False),
        sa.Column("last_seen", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_camera_health_camera_id"), "camera_health", ["camera_id"], unique=False)
    op.create_index(op.f("ix_camera_health_farm_id"), "camera_health", ["farm_id"], unique=False)
    op.create_index(op.f("ix_camera_health_id"), "camera_health", ["id"], unique=False)

    op.create_table(
        "edge_devices",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("farm_id", sa.String(length=20), nullable=False),
        sa.Column("device_name", sa.String(length=120), nullable=False),
        sa.Column("device_type", sa.String(length=60), nullable=False),
        sa.Column("serial_number", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("assigned_cameras", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_edge_devices_farm_id"), "edge_devices", ["farm_id"], unique=False)
    op.create_index(op.f("ix_edge_devices_id"), "edge_devices", ["id"], unique=False)

    op.create_table(
        "notification_gateways",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("farm_id", sa.String(length=20), nullable=False),
        sa.Column("gateway_type", sa.String(length=30), nullable=False),
        sa.Column("endpoint", sa.String(length=255), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_notification_gateways_farm_id"), "notification_gateways", ["farm_id"], unique=False)
    op.create_index(op.f("ix_notification_gateways_id"), "notification_gateways", ["id"], unique=False)

    op.create_table(
        "licenses",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("farm_id", sa.String(length=20), nullable=False),
        sa.Column("plan", sa.String(length=40), nullable=False),
        sa.Column("max_cameras", sa.Integer(), nullable=False),
        sa.Column("max_ai_models", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.String(length=20), nullable=False),
        sa.Column("end_date", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_licenses_farm_id"), "licenses", ["farm_id"], unique=False)
    op.create_index(op.f("ix_licenses_id"), "licenses", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_licenses_id"), table_name="licenses")
    op.drop_index(op.f("ix_licenses_farm_id"), table_name="licenses")
    op.drop_table("licenses")
    op.drop_index(op.f("ix_notification_gateways_id"), table_name="notification_gateways")
    op.drop_index(op.f("ix_notification_gateways_farm_id"), table_name="notification_gateways")
    op.drop_table("notification_gateways")
    op.drop_index(op.f("ix_edge_devices_id"), table_name="edge_devices")
    op.drop_index(op.f("ix_edge_devices_farm_id"), table_name="edge_devices")
    op.drop_table("edge_devices")
    op.drop_index(op.f("ix_camera_health_id"), table_name="camera_health")
    op.drop_index(op.f("ix_camera_health_farm_id"), table_name="camera_health")
    op.drop_index(op.f("ix_camera_health_camera_id"), table_name="camera_health")
    op.drop_table("camera_health")
    op.drop_index(op.f("ix_events_farm_id"), table_name="events")
    op.drop_column("events", "farm_id")
    op.drop_index(op.f("ix_cameras_farm_id"), table_name="cameras")
    op.drop_column("cameras", "farm_id")
    op.drop_index(op.f("ix_farms_id"), table_name="farms")
    op.drop_table("farms")
