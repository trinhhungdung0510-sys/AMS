"""event rule engine fields v1.3

Revision ID: 0029_event_rule_engine
Revises: 0028_zone_rules
Create Date: 2026-06-21 12:30:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0029_event_rule_engine"
down_revision: Optional[str] = "0028_zone_rules"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.add_column("events", sa.Column("zone_id", sa.String(length=24), nullable=True))
    op.add_column("events", sa.Column("rule_id", sa.String(length=24), nullable=True))
    op.add_column("events", sa.Column("event_type", sa.String(length=80), nullable=True))
    op.add_column("events", sa.Column("confidence_score", sa.Float(), nullable=True))
    op.add_column("events", sa.Column("snapshot_url", sa.String(length=500), nullable=True))
    op.add_column("events", sa.Column("started_at", sa.String(length=32), nullable=True))
    op.add_column("events", sa.Column("ended_at", sa.String(length=32), nullable=True))
    op.add_column("events", sa.Column("event_metadata", sa.JSON(), nullable=True))
    op.add_column("events", sa.Column("record_created_at", sa.String(length=32), nullable=True))
    op.create_index(op.f("ix_events_zone_id"), "events", ["zone_id"], unique=False)
    op.create_index(op.f("ix_events_rule_id"), "events", ["rule_id"], unique=False)
    op.execute("UPDATE events SET started_at = occurred_at WHERE started_at IS NULL")


def downgrade() -> None:
    op.drop_index(op.f("ix_events_rule_id"), table_name="events")
    op.drop_index(op.f("ix_events_zone_id"), table_name="events")
    op.drop_column("events", "record_created_at")
    op.drop_column("events", "event_metadata")
    op.drop_column("events", "ended_at")
    op.drop_column("events", "started_at")
    op.drop_column("events", "snapshot_url")
    op.drop_column("events", "confidence_score")
    op.drop_column("events", "event_type")
    op.drop_column("events", "rule_id")
    op.drop_column("events", "zone_id")
