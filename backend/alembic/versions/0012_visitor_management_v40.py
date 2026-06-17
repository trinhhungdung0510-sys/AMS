"""visitor management v40

Revision ID: 0012_visitor_management_v40
Revises: 0011_employee_management_v40
Create Date: 2026-06-17 21:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0012_visitor_management_v40"
down_revision: Optional[str] = "0011_employee_management_v40"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "visitors",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("visitor_name", sa.String(length=120), nullable=False),
        sa.Column("company", sa.String(length=120), nullable=False),
        sa.Column("vehicle_plate", sa.String(length=20), nullable=False),
        sa.Column("visit_purpose", sa.String(length=255), nullable=False),
        sa.Column("arrival_time", sa.String(length=32), nullable=True),
        sa.Column("departure_time", sa.String(length=32), nullable=True),
        sa.Column("approved_by", sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_visitors_id"), "visitors", ["id"], unique=False)
    op.create_index(op.f("ix_visitors_company"), "visitors", ["company"], unique=False)
    op.create_index(op.f("ix_visitors_vehicle_plate"), "visitors", ["vehicle_plate"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_visitors_vehicle_plate"), table_name="visitors")
    op.drop_index(op.f("ix_visitors_company"), table_name="visitors")
    op.drop_index(op.f("ix_visitors_id"), table_name="visitors")
    op.drop_table("visitors")
