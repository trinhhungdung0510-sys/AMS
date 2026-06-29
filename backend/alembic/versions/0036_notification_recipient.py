"""Add recipient to notification_deliveries.

Revision ID: 0036_notification_recipient
Revises: 0035_violation_notification
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0036_notification_recipient"
down_revision = "0035_violation_notification"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("notification_deliveries", sa.Column("recipient", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("notification_deliveries", "recipient")
