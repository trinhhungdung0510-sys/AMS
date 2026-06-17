"""animal intrusion engine v33

Revision ID: 0014_animal_intrusion_engine_v33
Revises: 0013_zone_crossing_engine_v32
Create Date: 2026-06-17 22:30:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0014_animal_intrusion_engine_v33"
down_revision: Optional[str] = "0013_zone_crossing_engine_v32"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "animal_intrusion_policies",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("object_type", sa.String(length=40), nullable=False),
        sa.Column("allowed_zones", sa.JSON(), nullable=False),
        sa.Column("restricted_zones", sa.JSON(), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("object_type"),
    )
    op.create_index(op.f("ix_animal_intrusion_policies_id"), "animal_intrusion_policies", ["id"], unique=False)
    op.create_index(
        op.f("ix_animal_intrusion_policies_object_type"),
        "animal_intrusion_policies",
        ["object_type"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_animal_intrusion_policies_object_type"), table_name="animal_intrusion_policies")
    op.drop_index(op.f("ix_animal_intrusion_policies_id"), table_name="animal_intrusion_policies")
    op.drop_table("animal_intrusion_policies")
