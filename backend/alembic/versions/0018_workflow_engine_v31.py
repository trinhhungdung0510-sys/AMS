"""workflow engine v3.1

Revision ID: 0018_workflow_engine_v31
Revises: 0017_biosecurity_zone_engine_v30
Create Date: 2026-06-18 01:00:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0018_workflow_engine_v31"
down_revision: Optional[str] = "0017_biosecurity_zone_engine_v30"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.add_column("workflows", sa.Column("created_at", sa.String(length=32), nullable=True))
    op.execute("UPDATE workflows SET created_at = '2026-06-17T00:00:00' WHERE created_at IS NULL")
    op.alter_column("workflows", "created_at", nullable=False)

    op.add_column(
        "workflow_steps",
        sa.Column("required", sa.Boolean(), server_default=sa.text("true"), nullable=False),
    )

    op.add_column("events", sa.Column("violation_code", sa.String(length=40), nullable=True))
    op.create_index(op.f("ix_events_violation_code"), "events", ["violation_code"], unique=False)

    op.create_table(
        "person_tracks",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("track_id", sa.Integer(), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("zone_id", sa.String(length=40), nullable=False),
        sa.Column("enter_time", sa.String(length=32), nullable=False),
        sa.Column("exit_time", sa.String(length=32), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_person_tracks_track_id"), "person_tracks", ["track_id"], unique=False)
    op.create_index(op.f("ix_person_tracks_camera_id"), "person_tracks", ["camera_id"], unique=False)
    op.create_index(op.f("ix_person_tracks_zone_id"), "person_tracks", ["zone_id"], unique=False)
    op.create_index(op.f("ix_person_tracks_enter_time"), "person_tracks", ["enter_time"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_person_tracks_enter_time"), table_name="person_tracks")
    op.drop_index(op.f("ix_person_tracks_zone_id"), table_name="person_tracks")
    op.drop_index(op.f("ix_person_tracks_camera_id"), table_name="person_tracks")
    op.drop_index(op.f("ix_person_tracks_track_id"), table_name="person_tracks")
    op.drop_table("person_tracks")
    op.drop_index(op.f("ix_events_violation_code"), table_name="events")
    op.drop_column("events", "violation_code")
    op.drop_column("workflow_steps", "required")
    op.drop_column("workflows", "created_at")
