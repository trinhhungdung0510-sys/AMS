"""biosecurity ai engine v4.0

Revision ID: 0019_biosecurity_ai_engine_v40
Revises: 0018_workflow_engine_v31
Create Date: 2026-06-18 02:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0019_biosecurity_ai_engine_v40"
down_revision: Optional[str] = "0018_workflow_engine_v31"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.add_column("biosecurity_rules", sa.Column("rule_type", sa.String(length=40), nullable=True))
    op.add_column("biosecurity_rules", sa.Column("evaluation_mode", sa.String(length=40), nullable=True))
    op.create_index(op.f("ix_biosecurity_rules_rule_type"), "biosecurity_rules", ["rule_type"], unique=False)

    op.add_column("zone_transitions", sa.Column("atsh_rule_code", sa.String(length=80), nullable=True))
    op.add_column("zone_transitions", sa.Column("atsh_severity", sa.String(length=20), nullable=True))
    op.create_index(op.f("ix_zone_transitions_atsh_rule_code"), "zone_transitions", ["atsh_rule_code"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_zone_transitions_atsh_rule_code"), table_name="zone_transitions")
    op.drop_column("zone_transitions", "atsh_severity")
    op.drop_column("zone_transitions", "atsh_rule_code")
    op.drop_index(op.f("ix_biosecurity_rules_rule_type"), table_name="biosecurity_rules")
    op.drop_column("biosecurity_rules", "evaluation_mode")
    op.drop_column("biosecurity_rules", "rule_type")
