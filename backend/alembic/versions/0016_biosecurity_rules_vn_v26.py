"""biosecurity rules vn v2.6

Revision ID: 0016_biosecurity_rules_vn_v26
Revises: 0015_workflow_engine_v34
Create Date: 2026-06-17 23:45:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0016_biosecurity_rules_vn_v26"
down_revision: Optional[str] = "0015_workflow_engine_v34"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.add_column("biosecurity_rules", sa.Column("rule_code", sa.String(length=80), nullable=True))
    op.add_column("biosecurity_rules", sa.Column("rule_name_vi", sa.String(length=160), nullable=True))
    op.add_column("biosecurity_rules", sa.Column("rule_name_en", sa.String(length=160), nullable=True))
    op.add_column("biosecurity_rules", sa.Column("category", sa.String(length=40), nullable=True))
    op.add_column("biosecurity_rules", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("biosecurity_rules", sa.Column("created_at", sa.String(length=32), nullable=True))

    op.execute(
        """
        UPDATE biosecurity_rules
        SET
            rule_code = UPPER(rule_type),
            rule_name_en = rule_name,
            rule_name_vi = rule_name,
            category = CASE
                WHEN object_type IN ('dog', 'cat', 'rat', 'bird') THEN 'animal'
                WHEN object_type = 'vehicle' THEN 'vehicle'
                WHEN object_type = 'person' THEN 'human'
                ELSE 'movement'
            END,
            description = rule_name,
            created_at = '2026-06-17T00:00:00+07:00'
        """
    )

    op.alter_column("biosecurity_rules", "rule_code", nullable=False)
    op.alter_column("biosecurity_rules", "rule_name_vi", nullable=False)
    op.alter_column("biosecurity_rules", "rule_name_en", nullable=False)
    op.alter_column("biosecurity_rules", "category", nullable=False)
    op.alter_column("biosecurity_rules", "description", nullable=False, server_default="")
    op.alter_column("biosecurity_rules", "created_at", nullable=False)
    op.alter_column("biosecurity_rules", "object_type", existing_type=sa.String(length=40), nullable=True)
    op.alter_column("biosecurity_rules", "from_zone", existing_type=sa.String(length=40), nullable=True)
    op.alter_column("biosecurity_rules", "to_zone", existing_type=sa.String(length=40), nullable=True)

    op.drop_index(op.f("ix_biosecurity_rules_rule_type"), table_name="biosecurity_rules")
    op.drop_column("biosecurity_rules", "rule_name")
    op.drop_column("biosecurity_rules", "rule_type")

    op.create_index(op.f("ix_biosecurity_rules_rule_code"), "biosecurity_rules", ["rule_code"], unique=False)
    op.create_index(op.f("ix_biosecurity_rules_category"), "biosecurity_rules", ["category"], unique=False)

    op.alter_column("biosecurity_rules", "description", server_default=None)


def downgrade() -> None:
    op.add_column("biosecurity_rules", sa.Column("rule_type", sa.String(length=80), nullable=True))
    op.add_column("biosecurity_rules", sa.Column("rule_name", sa.String(length=160), nullable=True))

    op.execute(
        """
        UPDATE biosecurity_rules
        SET
            rule_type = LOWER(rule_code),
            rule_name = rule_name_en
        """
    )

    op.alter_column("biosecurity_rules", "rule_type", nullable=False)
    op.alter_column("biosecurity_rules", "rule_name", nullable=False)
    op.alter_column("biosecurity_rules", "object_type", existing_type=sa.String(length=40), nullable=False)
    op.alter_column("biosecurity_rules", "from_zone", existing_type=sa.String(length=40), nullable=False)
    op.alter_column("biosecurity_rules", "to_zone", existing_type=sa.String(length=40), nullable=False)

    op.drop_index(op.f("ix_biosecurity_rules_category"), table_name="biosecurity_rules")
    op.drop_index(op.f("ix_biosecurity_rules_rule_code"), table_name="biosecurity_rules")
    op.drop_column("biosecurity_rules", "created_at")
    op.drop_column("biosecurity_rules", "description")
    op.drop_column("biosecurity_rules", "category")
    op.drop_column("biosecurity_rules", "rule_name_en")
    op.drop_column("biosecurity_rules", "rule_name_vi")
    op.drop_column("biosecurity_rules", "rule_code")

    op.create_index(op.f("ix_biosecurity_rules_rule_type"), "biosecurity_rules", ["rule_type"], unique=False)
