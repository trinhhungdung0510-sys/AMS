"""biosecurity zone engine v3.0

Revision ID: 0017_biosecurity_zone_engine_v30
Revises: 0016_biosecurity_rules_vn_v26
Create Date: 2026-06-18 00:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0017_biosecurity_zone_engine_v30"
down_revision: Optional[str] = "0016_biosecurity_rules_vn_v26"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.add_column("zone_polygons", sa.Column("biosecurity_level", sa.String(length=20), nullable=True))
    op.execute("UPDATE zone_polygons SET biosecurity_level = 'yellow' WHERE biosecurity_level IS NULL")
    op.alter_column("zone_polygons", "biosecurity_level", nullable=False)
    op.create_index(
        op.f("ix_zone_polygons_biosecurity_level"),
        "zone_polygons",
        ["biosecurity_level"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_zone_polygons_biosecurity_level"), table_name="zone_polygons")
    op.drop_column("zone_polygons", "biosecurity_level")
