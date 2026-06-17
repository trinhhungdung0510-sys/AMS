"""zone crossing engine v32

Revision ID: 0013_zone_crossing_engine_v32
Revises: 0012_visitor_management_v40
Create Date: 2026-06-17 21:30:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0013_zone_crossing_engine_v32"
down_revision: Optional[str] = "0012_visitor_management_v40"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.add_column(
        "zone_transitions",
        sa.Column("camera_id", sa.String(length=20), server_default="CAM-001", nullable=False),
    )
    op.add_column(
        "zone_transitions",
        sa.Column("cross_time", sa.String(length=32), server_default="", nullable=False),
    )
    op.execute("UPDATE zone_transitions SET cross_time = timestamp WHERE cross_time = ''")
    op.create_index(op.f("ix_zone_transitions_camera_id"), "zone_transitions", ["camera_id"], unique=False)
    op.create_index(op.f("ix_zone_transitions_cross_time"), "zone_transitions", ["cross_time"], unique=False)
    op.alter_column("zone_transitions", "camera_id", server_default=None)
    op.alter_column("zone_transitions", "cross_time", server_default=None)


def downgrade() -> None:
    op.drop_index(op.f("ix_zone_transitions_cross_time"), table_name="zone_transitions")
    op.drop_index(op.f("ix_zone_transitions_camera_id"), table_name="zone_transitions")
    op.drop_column("zone_transitions", "cross_time")
    op.drop_column("zone_transitions", "camera_id")
