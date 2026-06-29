"""Add smtp_latency_ms to notification_deliveries.

Revision ID: 0037_gmail_delivery_latency
Revises: 0036_notification_recipient
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0037_gmail_delivery_latency"
down_revision = "0036_notification_recipient"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("notification_deliveries", sa.Column("smtp_latency_ms", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("notification_deliveries", "smtp_latency_ms")
