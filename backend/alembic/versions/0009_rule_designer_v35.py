"""rule designer v35

Revision ID: 0009_rule_designer_v35
Revises: 0008_biosecurity_rule_engine
Create Date: 2026-06-17 18:44:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0009_rule_designer_v35"
down_revision: Optional[str] = "0008_biosecurity_rule_engine"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.add_column("biosecurity_rules", sa.Column("object_type", sa.String(length=40), server_default="person", nullable=False))
    op.add_column("biosecurity_rules", sa.Column("from_zone", sa.String(length=40), server_default="any_zone", nullable=False))
    op.add_column("biosecurity_rules", sa.Column("to_zone", sa.String(length=40), server_default="any_zone", nullable=False))
    op.add_column("biosecurity_rules", sa.Column("required_zone", sa.String(length=40), nullable=True))
    op.create_index(op.f("ix_biosecurity_rules_object_type"), "biosecurity_rules", ["object_type"], unique=False)
    op.create_index(op.f("ix_biosecurity_rules_from_zone"), "biosecurity_rules", ["from_zone"], unique=False)
    op.create_index(op.f("ix_biosecurity_rules_to_zone"), "biosecurity_rules", ["to_zone"], unique=False)

    op.execute(
        """
        UPDATE biosecurity_rules
        SET object_type = 'person', from_zone = 'dirty_zone', to_zone = 'safe_zone', required_zone = 'disinfection_zone'
        WHERE id = 'BR-001'
        """
    )
    op.execute(
        """
        UPDATE biosecurity_rules
        SET object_type = 'vehicle', from_zone = 'outside_zone', to_zone = 'production_zone', required_zone = 'vehicle_disinfection_zone'
        WHERE id = 'BR-002'
        """
    )
    op.execute(
        """
        UPDATE biosecurity_rules
        SET object_type = 'dog', from_zone = 'any_zone', to_zone = 'production_zone', required_zone = NULL
        WHERE id = 'BR-003'
        """
    )
    op.execute(
        """
        UPDATE biosecurity_rules
        SET object_type = 'cat', from_zone = 'any_zone', to_zone = 'production_zone', required_zone = NULL
        WHERE id = 'BR-004'
        """
    )
    op.execute(
        """
        UPDATE biosecurity_rules
        SET object_type = 'bird', from_zone = 'any_zone', to_zone = 'feed_storage_zone', required_zone = NULL
        WHERE id = 'BR-005'
        """
    )

    op.alter_column("biosecurity_rules", "object_type", server_default=None)
    op.alter_column("biosecurity_rules", "from_zone", server_default=None)
    op.alter_column("biosecurity_rules", "to_zone", server_default=None)


def downgrade() -> None:
    op.drop_index(op.f("ix_biosecurity_rules_to_zone"), table_name="biosecurity_rules")
    op.drop_index(op.f("ix_biosecurity_rules_from_zone"), table_name="biosecurity_rules")
    op.drop_index(op.f("ix_biosecurity_rules_object_type"), table_name="biosecurity_rules")
    op.drop_column("biosecurity_rules", "required_zone")
    op.drop_column("biosecurity_rules", "to_zone")
    op.drop_column("biosecurity_rules", "from_zone")
    op.drop_column("biosecurity_rules", "object_type")
