"""zone rules for camera rule engine v1.3

Revision ID: 0028_zone_rules
Revises: 0027_zone_reference_dims
Create Date: 2026-06-21 12:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0028_zone_rules"
down_revision: Optional[str] = "0027_zone_reference_dims"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "zone_rules",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("zone_id", sa.String(length=24), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("rule_type", sa.String(length=40), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("cooldown_seconds", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.Column("updated_at", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_zone_rules_camera_id"), "zone_rules", ["camera_id"], unique=False)
    op.create_index(op.f("ix_zone_rules_id"), "zone_rules", ["id"], unique=False)
    op.create_index(op.f("ix_zone_rules_zone_id"), "zone_rules", ["zone_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_zone_rules_zone_id"), table_name="zone_rules")
    op.drop_index(op.f("ix_zone_rules_id"), table_name="zone_rules")
    op.drop_index(op.f("ix_zone_rules_camera_id"), table_name="zone_rules")
    op.drop_table("zone_rules")
