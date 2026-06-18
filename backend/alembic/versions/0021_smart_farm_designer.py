"""smart farm designer tables

Revision ID: 0021_smart_farm_designer
Revises: 0020_farm_map_editor
Create Date: 2026-06-18 14:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0021_smart_farm_designer"
down_revision: Optional[str] = "0020_farm_map_editor"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "farm_layouts",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("farm_id", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("address", sa.Text(), nullable=False, server_default=""),
        sa.Column("center_lat", sa.Float(), nullable=False),
        sa.Column("center_lng", sa.Float(), nullable=False),
        sa.Column("zoom", sa.Integer(), nullable=False, server_default=sa.text("17")),
        sa.Column("base_layer", sa.String(length=20), nullable=False, server_default="satellite"),
        sa.Column("is_template", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_farm_layouts_farm_id"), "farm_layouts", ["farm_id"], unique=False)
    op.create_index(op.f("ix_farm_layouts_id"), "farm_layouts", ["id"], unique=False)

    op.create_table(
        "farm_objects",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("layout_id", sa.String(length=20), nullable=False),
        sa.Column("object_type", sa.String(length=40), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
        sa.Column("width", sa.Float(), nullable=False, server_default=sa.text("0.0003")),
        sa.Column("height", sa.Float(), nullable=False, server_default=sa.text("0.0003")),
        sa.Column("rotation", sa.Float(), nullable=False, server_default=sa.text("0")),
        sa.Column("atsh_zone_type", sa.String(length=30), nullable=False, server_default="buffer"),
        sa.Column("atsh_level", sa.String(length=20), nullable=False, server_default="green"),
        sa.Column("linked_camera_id", sa.String(length=20), nullable=True),
        sa.Column("linked_zone_id", sa.String(length=20), nullable=True),
        sa.Column("camera_direction", sa.Float(), nullable=True),
        sa.Column("camera_fov", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.ForeignKeyConstraint(["layout_id"], ["farm_layouts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_farm_objects_id"), "farm_objects", ["id"], unique=False)
    op.create_index(op.f("ix_farm_objects_layout_id"), "farm_objects", ["layout_id"], unique=False)

    op.create_table(
        "farm_routes",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("layout_id", sa.String(length=20), nullable=False),
        sa.Column("route_type", sa.String(length=30), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("points", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("labels", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("valid", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.ForeignKeyConstraint(["layout_id"], ["farm_layouts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_farm_routes_id"), "farm_routes", ["id"], unique=False)
    op.create_index(op.f("ix_farm_routes_layout_id"), "farm_routes", ["layout_id"], unique=False)

    op.create_table(
        "farm_map_layers",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("layout_id", sa.String(length=20), nullable=False),
        sa.Column("layer_key", sa.String(length=30), nullable=False),
        sa.Column("visible", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("opacity", sa.Float(), nullable=False, server_default=sa.text("1")),
        sa.ForeignKeyConstraint(["layout_id"], ["farm_layouts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_farm_map_layers_id"), "farm_map_layers", ["id"], unique=False)
    op.create_index(op.f("ix_farm_map_layers_layout_id"), "farm_map_layers", ["layout_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_farm_map_layers_layout_id"), table_name="farm_map_layers")
    op.drop_index(op.f("ix_farm_map_layers_id"), table_name="farm_map_layers")
    op.drop_table("farm_map_layers")
    op.drop_index(op.f("ix_farm_routes_layout_id"), table_name="farm_routes")
    op.drop_index(op.f("ix_farm_routes_id"), table_name="farm_routes")
    op.drop_table("farm_routes")
    op.drop_index(op.f("ix_farm_objects_layout_id"), table_name="farm_objects")
    op.drop_index(op.f("ix_farm_objects_id"), table_name="farm_objects")
    op.drop_table("farm_objects")
    op.drop_index(op.f("ix_farm_layouts_id"), table_name="farm_layouts")
    op.drop_index(op.f("ix_farm_layouts_farm_id"), table_name="farm_layouts")
    op.drop_table("farm_layouts")
