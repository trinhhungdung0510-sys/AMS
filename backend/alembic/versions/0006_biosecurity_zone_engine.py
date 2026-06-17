"""biosecurity zone engine

Revision ID: 0006_biosecurity_zone_engine
Revises: 0005_enterprise_multi_farm
Create Date: 2026-06-17 18:17:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0006_biosecurity_zone_engine"
down_revision: Optional[str] = "0005_enterprise_multi_farm"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "zone_polygons",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("farm_id", sa.String(length=20), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("zone_name", sa.String(length=120), nullable=False),
        sa.Column("zone_type", sa.String(length=40), nullable=False),
        sa.Column("color", sa.String(length=20), nullable=False),
        sa.Column("polygon_points", sa.JSON(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_zone_polygons_camera_id"), "zone_polygons", ["camera_id"], unique=False)
    op.create_index(op.f("ix_zone_polygons_farm_id"), "zone_polygons", ["farm_id"], unique=False)
    op.create_index(op.f("ix_zone_polygons_id"), "zone_polygons", ["id"], unique=False)
    op.create_index(op.f("ix_zone_polygons_zone_type"), "zone_polygons", ["zone_type"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_zone_polygons_zone_type"), table_name="zone_polygons")
    op.drop_index(op.f("ix_zone_polygons_id"), table_name="zone_polygons")
    op.drop_index(op.f("ix_zone_polygons_farm_id"), table_name="zone_polygons")
    op.drop_index(op.f("ix_zone_polygons_camera_id"), table_name="zone_polygons")
    op.drop_table("zone_polygons")
