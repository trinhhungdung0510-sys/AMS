"""zone designer opacity and description

Revision ID: 0022_zone_designer_opacity
Revises: 0021_smart_farm_designer
Create Date: 2026-06-18 16:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0022_zone_designer_opacity"
down_revision: Optional[str] = "0021_smart_farm_designer"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.add_column(
        "zone_polygons",
        sa.Column("opacity", sa.Float(), nullable=False, server_default="0.3"),
    )
    op.add_column(
        "zone_polygons",
        sa.Column("description", sa.String(length=500), nullable=False, server_default=""),
    )


def downgrade() -> None:
    op.drop_column("zone_polygons", "description")
    op.drop_column("zone_polygons", "opacity")
