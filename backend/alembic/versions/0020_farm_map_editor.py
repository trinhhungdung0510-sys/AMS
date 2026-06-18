"""farm map editor layout and object geometry

Revision ID: 0020_farm_map_editor
Revises: 0019_biosecurity_ai_engine_v40
Create Date: 2026-06-18 12:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0020_farm_map_editor"
down_revision: Optional[str] = "0019_biosecurity_ai_engine_v40"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "farm_map_layouts",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("farm_id", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("is_template", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("center_lat", sa.Float(), nullable=False),
        sa.Column("center_lng", sa.Float(), nullable=False),
        sa.Column("zoom", sa.Integer(), nullable=False, server_default=sa.text("17")),
        sa.Column("base_layer", sa.String(length=20), nullable=False, server_default="satellite"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_farm_map_layouts_farm_id"), "farm_map_layouts", ["farm_id"], unique=False)
    op.create_index(op.f("ix_farm_map_layouts_id"), "farm_map_layouts", ["id"], unique=False)

    op.add_column("farm_map_objects", sa.Column("layout_id", sa.String(length=20), nullable=True))
    op.add_column("farm_map_objects", sa.Column("description", sa.Text(), nullable=False, server_default=""))
    op.add_column("farm_map_objects", sa.Column("width", sa.Float(), nullable=False, server_default=sa.text("0.0003")))
    op.add_column("farm_map_objects", sa.Column("height", sa.Float(), nullable=False, server_default=sa.text("0.0003")))
    op.add_column("farm_map_objects", sa.Column("rotation", sa.Float(), nullable=False, server_default=sa.text("0")))
    op.add_column("farm_map_objects", sa.Column("atsh_zone_type", sa.String(length=30), nullable=False, server_default="buffer"))
    op.add_column("farm_map_objects", sa.Column("atsh_level", sa.String(length=20), nullable=False, server_default="green"))
    op.add_column("farm_map_objects", sa.Column("linked_camera_id", sa.String(length=20), nullable=True))
    op.add_column("farm_map_objects", sa.Column("linked_zone_id", sa.String(length=20), nullable=True))
    op.add_column("farm_map_objects", sa.Column("camera_direction", sa.Float(), nullable=True))
    op.add_column("farm_map_objects", sa.Column("camera_fov", sa.Float(), nullable=True))
    op.create_foreign_key(
        "fk_farm_map_objects_layout_id",
        "farm_map_objects",
        "farm_map_layouts",
        ["layout_id"],
        ["id"],
    )
    op.create_index(op.f("ix_farm_map_objects_layout_id"), "farm_map_objects", ["layout_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_farm_map_objects_layout_id"), table_name="farm_map_objects")
    op.drop_constraint("fk_farm_map_objects_layout_id", "farm_map_objects", type_="foreignkey")
    op.drop_column("farm_map_objects", "camera_fov")
    op.drop_column("farm_map_objects", "camera_direction")
    op.drop_column("farm_map_objects", "linked_zone_id")
    op.drop_column("farm_map_objects", "linked_camera_id")
    op.drop_column("farm_map_objects", "atsh_level")
    op.drop_column("farm_map_objects", "atsh_zone_type")
    op.drop_column("farm_map_objects", "rotation")
    op.drop_column("farm_map_objects", "height")
    op.drop_column("farm_map_objects", "width")
    op.drop_column("farm_map_objects", "description")
    op.drop_column("farm_map_objects", "layout_id")
    op.drop_index(op.f("ix_farm_map_layouts_id"), table_name="farm_map_layouts")
    op.drop_index(op.f("ix_farm_map_layouts_farm_id"), table_name="farm_map_layouts")
    op.drop_table("farm_map_layouts")
