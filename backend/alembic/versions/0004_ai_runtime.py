"""ai runtime

Revision ID: 0004_ai_runtime
Revises: 0003_ai_ready_modules
Create Date: 2026-06-17 17:05:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0004_ai_runtime"
down_revision: Optional[str] = "0003_ai_ready_modules"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "ai_tasks",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("camera_id", sa.String(length=20), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("result", sa.Text(), nullable=False),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.Column("processed_at", sa.String(length=32), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_tasks_camera_id"), "ai_tasks", ["camera_id"], unique=False)
    op.create_index(op.f("ix_ai_tasks_id"), "ai_tasks", ["id"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(length=24), nullable=False),
        sa.Column("user_id", sa.String(length=20), nullable=False),
        sa.Column("action", sa.String(length=80), nullable=False),
        sa.Column("resource_type", sa.String(length=80), nullable=False),
        sa.Column("resource_id", sa.String(length=80), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_logs_id"), "audit_logs", ["id"], unique=False)
    op.create_index(op.f("ix_audit_logs_user_id"), "audit_logs", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_logs_user_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_id"), table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index(op.f("ix_ai_tasks_id"), table_name="ai_tasks")
    op.drop_index(op.f("ix_ai_tasks_camera_id"), table_name="ai_tasks")
    op.drop_table("ai_tasks")
