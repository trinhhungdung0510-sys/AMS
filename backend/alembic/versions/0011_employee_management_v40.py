"""employee management v40

Revision ID: 0011_employee_management_v40
Revises: 0010_farm_layout_template
Create Date: 2026-06-17 20:30:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0011_employee_management_v40"
down_revision: Optional[str] = "0010_farm_layout_template"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "employees",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("employee_code", sa.String(length=40), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("department", sa.String(length=80), nullable=False),
        sa.Column("assigned_zone", sa.String(length=40), nullable=False),
        sa.Column("uniform_color", sa.String(length=40), nullable=False),
        sa.Column("face_image", sa.String(length=255), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("employee_code"),
    )
    op.create_index(op.f("ix_employees_id"), "employees", ["id"], unique=False)
    op.create_index(op.f("ix_employees_employee_code"), "employees", ["employee_code"], unique=False)
    op.create_index(op.f("ix_employees_department"), "employees", ["department"], unique=False)
    op.create_index(op.f("ix_employees_assigned_zone"), "employees", ["assigned_zone"], unique=False)

    op.create_table(
        "object_tracks",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("track_id", sa.Integer(), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("object_type", sa.String(length=40), nullable=False),
        sa.Column("current_zone", sa.String(length=40), nullable=False),
        sa.Column("previous_zone", sa.String(length=40), nullable=True),
        sa.Column("employee_id", sa.String(length=24), nullable=True),
        sa.Column("enter_time", sa.String(length=32), nullable=False),
        sa.Column("leave_time", sa.String(length=32), nullable=True),
        sa.Column("last_seen", sa.String(length=32), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_object_tracks_id"), "object_tracks", ["id"], unique=False)
    op.create_index(op.f("ix_object_tracks_track_id"), "object_tracks", ["track_id"], unique=False)
    op.create_index(op.f("ix_object_tracks_camera_id"), "object_tracks", ["camera_id"], unique=False)
    op.create_index(op.f("ix_object_tracks_object_type"), "object_tracks", ["object_type"], unique=False)
    op.create_index(op.f("ix_object_tracks_current_zone"), "object_tracks", ["current_zone"], unique=False)
    op.create_index(op.f("ix_object_tracks_employee_id"), "object_tracks", ["employee_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_object_tracks_employee_id"), table_name="object_tracks")
    op.drop_index(op.f("ix_object_tracks_current_zone"), table_name="object_tracks")
    op.drop_index(op.f("ix_object_tracks_object_type"), table_name="object_tracks")
    op.drop_index(op.f("ix_object_tracks_camera_id"), table_name="object_tracks")
    op.drop_index(op.f("ix_object_tracks_track_id"), table_name="object_tracks")
    op.drop_index(op.f("ix_object_tracks_id"), table_name="object_tracks")
    op.drop_table("object_tracks")

    op.drop_index(op.f("ix_employees_assigned_zone"), table_name="employees")
    op.drop_index(op.f("ix_employees_department"), table_name="employees")
    op.drop_index(op.f("ix_employees_employee_code"), table_name="employees")
    op.drop_index(op.f("ix_employees_id"), table_name="employees")
    op.drop_table("employees")
