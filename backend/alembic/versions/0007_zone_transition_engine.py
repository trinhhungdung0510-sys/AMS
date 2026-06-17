"""zone transition engine

Revision ID: 0007_zone_transition_engine
Revises: 0006_biosecurity_zone_engine
Create Date: 2026-06-17 18:26:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0007_zone_transition_engine"
down_revision: Optional[str] = "0006_biosecurity_zone_engine"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "zone_transitions",
        sa.Column("id", sa.String(length=28), nullable=False),
        sa.Column("object_type", sa.String(length=40), nullable=False),
        sa.Column("track_id", sa.Integer(), nullable=False),
        sa.Column("from_zone", sa.String(length=40), nullable=False),
        sa.Column("to_zone", sa.String(length=40), nullable=False),
        sa.Column("timestamp", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_zone_transitions_from_zone"), "zone_transitions", ["from_zone"], unique=False)
    op.create_index(op.f("ix_zone_transitions_id"), "zone_transitions", ["id"], unique=False)
    op.create_index(op.f("ix_zone_transitions_object_type"), "zone_transitions", ["object_type"], unique=False)
    op.create_index(op.f("ix_zone_transitions_timestamp"), "zone_transitions", ["timestamp"], unique=False)
    op.create_index(op.f("ix_zone_transitions_to_zone"), "zone_transitions", ["to_zone"], unique=False)
    op.create_index(op.f("ix_zone_transitions_track_id"), "zone_transitions", ["track_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_zone_transitions_track_id"), table_name="zone_transitions")
    op.drop_index(op.f("ix_zone_transitions_to_zone"), table_name="zone_transitions")
    op.drop_index(op.f("ix_zone_transitions_timestamp"), table_name="zone_transitions")
    op.drop_index(op.f("ix_zone_transitions_object_type"), table_name="zone_transitions")
    op.drop_index(op.f("ix_zone_transitions_id"), table_name="zone_transitions")
    op.drop_index(op.f("ix_zone_transitions_from_zone"), table_name="zone_transitions")
    op.drop_table("zone_transitions")
