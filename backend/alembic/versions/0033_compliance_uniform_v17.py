"""compliance uniform templates v1.7 phase 3

Revision ID: 0033_compliance_uniform_v17
Revises: 0032_obs_schema_version
Create Date: 2026-06-18 12:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0033_compliance_uniform_v17"
down_revision: Optional[str] = "0032_obs_schema_version"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "uniform_templates",
        sa.Column("id", sa.String(length=24), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("image_paths", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.Column("updated_at", sa.String(length=32), nullable=False),
    )
    op.add_column(
        "camera_zones",
        sa.Column("required_uniform_id", sa.String(length=24), nullable=True),
    )
    op.create_index("ix_camera_zones_required_uniform_id", "camera_zones", ["required_uniform_id"])


def downgrade() -> None:
    op.drop_index("ix_camera_zones_required_uniform_id", table_name="camera_zones")
    op.drop_column("camera_zones", "required_uniform_id")
    op.drop_table("uniform_templates")
