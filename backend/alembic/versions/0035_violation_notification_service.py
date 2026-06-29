"""AMS v1.7 violation notification delivery log.

Revision ID: 0035_violation_notification
Revises: 0034_v19_rc1
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0035_violation_notification"
down_revision = "0034_v19_rc1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "notification_dispatches",
        sa.Column("event_id", sa.String(length=20), nullable=False),
        sa.Column("farm_id", sa.String(length=20), nullable=False),
        sa.Column("dispatched_at", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_index("ix_notification_dispatches_farm_id", "notification_dispatches", ["farm_id"])

    op.create_table(
        "notification_deliveries",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("event_id", sa.String(length=20), nullable=False),
        sa.Column("farm_id", sa.String(length=20), nullable=False),
        sa.Column("channel", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("sent_at", sa.String(length=32), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id", "channel", name="uq_notification_delivery_event_channel"),
    )
    op.create_index("ix_notification_deliveries_event_id", "notification_deliveries", ["event_id"])
    op.create_index("ix_notification_deliveries_farm_id", "notification_deliveries", ["farm_id"])


def downgrade() -> None:
    op.drop_index("ix_notification_deliveries_farm_id", table_name="notification_deliveries")
    op.drop_index("ix_notification_deliveries_event_id", table_name="notification_deliveries")
    op.drop_table("notification_deliveries")
    op.drop_index("ix_notification_dispatches_farm_id", table_name="notification_dispatches")
    op.drop_table("notification_dispatches")
