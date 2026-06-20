"""observation schema version column v1.5.1

Revision ID: 0032_obs_schema_version
Revises: 0031_rule_config_v14
Create Date: 2026-06-23 10:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0032_obs_schema_version"
down_revision: Optional[str] = "0031_rule_config_v14"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.add_column(
        "observations",
        sa.Column("schema_version", sa.String(length=8), nullable=False, server_default="v1"),
    )


def downgrade() -> None:
    op.drop_column("observations", "schema_version")
