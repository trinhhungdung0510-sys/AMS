"""biosecurity rule engine

Revision ID: 0008_biosecurity_rule_engine
Revises: 0007_zone_transition_engine
Create Date: 2026-06-17 18:32:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0008_biosecurity_rule_engine"
down_revision: Optional[str] = "0007_zone_transition_engine"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "biosecurity_rules",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("rule_name", sa.String(length=160), nullable=False),
        sa.Column("rule_type", sa.String(length=80), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_biosecurity_rules_id"), "biosecurity_rules", ["id"], unique=False)
    op.create_index(op.f("ix_biosecurity_rules_rule_type"), "biosecurity_rules", ["rule_type"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_biosecurity_rules_rule_type"), table_name="biosecurity_rules")
    op.drop_index(op.f("ix_biosecurity_rules_id"), table_name="biosecurity_rules")
    op.drop_table("biosecurity_rules")
