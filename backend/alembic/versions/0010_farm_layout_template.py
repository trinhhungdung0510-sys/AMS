"""farm layout template v35

Revision ID: 0010_farm_layout_template
Revises: 0009_rule_designer_v35
Create Date: 2026-06-17 19:30:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0010_farm_layout_template"
down_revision: Optional[str] = "0009_rule_designer_v35"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "farm_layout_templates",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_farm_layout_templates_id"), "farm_layout_templates", ["id"], unique=False)

    op.create_table(
        "template_zone_definitions",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("template_id", sa.String(length=24), nullable=False),
        sa.Column("zone_code", sa.String(length=40), nullable=False),
        sa.Column("zone_name", sa.String(length=120), nullable=False),
        sa.Column("zone_category", sa.String(length=40), nullable=False),
        sa.Column("biosecurity_level", sa.String(length=20), nullable=False),
        sa.Column("risk_level", sa.String(length=20), nullable=False),
        sa.Column("color", sa.String(length=20), nullable=False),
        sa.Column("layout_x", sa.Float(), nullable=False),
        sa.Column("layout_y", sa.Float(), nullable=False),
        sa.Column("layout_w", sa.Float(), nullable=False),
        sa.Column("layout_h", sa.Float(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_template_zone_definitions_id"), "template_zone_definitions", ["id"], unique=False)
    op.create_index(
        op.f("ix_template_zone_definitions_template_id"),
        "template_zone_definitions",
        ["template_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_template_zone_definitions_zone_code"),
        "template_zone_definitions",
        ["zone_code"],
        unique=False,
    )
    op.create_index(
        op.f("ix_template_zone_definitions_zone_category"),
        "template_zone_definitions",
        ["zone_category"],
        unique=False,
    )
    op.create_index(
        op.f("ix_template_zone_definitions_biosecurity_level"),
        "template_zone_definitions",
        ["biosecurity_level"],
        unique=False,
    )
    op.create_index(
        op.f("ix_template_zone_definitions_risk_level"),
        "template_zone_definitions",
        ["risk_level"],
        unique=False,
    )

    op.add_column("farm_zones", sa.Column("farm_id", sa.String(length=20), nullable=True))
    op.add_column("farm_zones", sa.Column("template_id", sa.String(length=24), nullable=True))
    op.add_column("farm_zones", sa.Column("template_zone_id", sa.String(length=24), nullable=True))
    op.add_column(
        "farm_zones",
        sa.Column("zone_code", sa.String(length=40), server_default="legacy_zone", nullable=False),
    )
    op.add_column(
        "farm_zones",
        sa.Column("zone_category", sa.String(length=40), server_default="legacy", nullable=False),
    )
    op.add_column(
        "farm_zones",
        sa.Column("biosecurity_level", sa.String(length=20), server_default="neutral", nullable=False),
    )
    op.add_column("farm_zones", sa.Column("layout_x", sa.Float(), nullable=True))
    op.add_column("farm_zones", sa.Column("layout_y", sa.Float(), nullable=True))
    op.add_column("farm_zones", sa.Column("layout_w", sa.Float(), nullable=True))
    op.add_column("farm_zones", sa.Column("layout_h", sa.Float(), nullable=True))
    op.add_column("farm_zones", sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False))
    op.add_column("farm_zones", sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False))

    op.create_index(op.f("ix_farm_zones_farm_id"), "farm_zones", ["farm_id"], unique=False)
    op.create_index(op.f("ix_farm_zones_template_id"), "farm_zones", ["template_id"], unique=False)
    op.create_index(op.f("ix_farm_zones_template_zone_id"), "farm_zones", ["template_zone_id"], unique=False)
    op.create_index(op.f("ix_farm_zones_zone_code"), "farm_zones", ["zone_code"], unique=False)
    op.create_index(op.f("ix_farm_zones_zone_category"), "farm_zones", ["zone_category"], unique=False)
    op.create_index(op.f("ix_farm_zones_biosecurity_level"), "farm_zones", ["biosecurity_level"], unique=False)

    op.alter_column("farm_zones", "zone_code", server_default=None)
    op.alter_column("farm_zones", "zone_category", server_default=None)
    op.alter_column("farm_zones", "biosecurity_level", server_default=None)
    op.alter_column("farm_zones", "sort_order", server_default=None)
    op.alter_column("farm_zones", "active", server_default=None)


def downgrade() -> None:
    op.drop_index(op.f("ix_farm_zones_biosecurity_level"), table_name="farm_zones")
    op.drop_index(op.f("ix_farm_zones_zone_category"), table_name="farm_zones")
    op.drop_index(op.f("ix_farm_zones_zone_code"), table_name="farm_zones")
    op.drop_index(op.f("ix_farm_zones_template_zone_id"), table_name="farm_zones")
    op.drop_index(op.f("ix_farm_zones_template_id"), table_name="farm_zones")
    op.drop_index(op.f("ix_farm_zones_farm_id"), table_name="farm_zones")
    op.drop_column("farm_zones", "active")
    op.drop_column("farm_zones", "sort_order")
    op.drop_column("farm_zones", "layout_h")
    op.drop_column("farm_zones", "layout_w")
    op.drop_column("farm_zones", "layout_y")
    op.drop_column("farm_zones", "layout_x")
    op.drop_column("farm_zones", "biosecurity_level")
    op.drop_column("farm_zones", "zone_category")
    op.drop_column("farm_zones", "zone_code")
    op.drop_column("farm_zones", "template_zone_id")
    op.drop_column("farm_zones", "template_id")
    op.drop_column("farm_zones", "farm_id")

    op.drop_index(op.f("ix_template_zone_definitions_risk_level"), table_name="template_zone_definitions")
    op.drop_index(op.f("ix_template_zone_definitions_biosecurity_level"), table_name="template_zone_definitions")
    op.drop_index(op.f("ix_template_zone_definitions_zone_category"), table_name="template_zone_definitions")
    op.drop_index(op.f("ix_template_zone_definitions_zone_code"), table_name="template_zone_definitions")
    op.drop_index(op.f("ix_template_zone_definitions_template_id"), table_name="template_zone_definitions")
    op.drop_index(op.f("ix_template_zone_definitions_id"), table_name="template_zone_definitions")
    op.drop_table("template_zone_definitions")

    op.drop_index(op.f("ix_farm_layout_templates_id"), table_name="farm_layout_templates")
    op.drop_table("farm_layout_templates")
