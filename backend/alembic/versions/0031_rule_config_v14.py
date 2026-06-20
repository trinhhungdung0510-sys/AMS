"""zone rule config json for evaluator v1.4

Revision ID: 0031_rule_config_v14
Revises: 0030_observations_v14
Create Date: 2026-06-22 10:05:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0031_rule_config_v14"
down_revision: Optional[str] = "0030_observations_v14"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.add_column(
        "zone_rules",
        sa.Column("config", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
    )


def downgrade() -> None:
    op.drop_column("zone_rules", "config")
