"""auth categories dashboard

Revision ID: 0002_auth_categories_dashboard
Revises: 0001_initial_ams_tables
Create Date: 2026-06-17 16:55:00
"""

from collections.abc import Sequence
from typing import Optional, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002_auth_categories_dashboard"
down_revision: Optional[str] = "0001_initial_ams_tables"
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


def upgrade() -> None:
    op.create_table(
        "alert_categories",
        sa.Column("code", sa.String(length=80), nullable=False),
        sa.Column("label", sa.String(length=160), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("code"),
    )
    op.create_index(op.f("ix_alert_categories_code"), "alert_categories", ["code"], unique=False)

    op.create_table(
        "token_blacklist",
        sa.Column("jti", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=20), nullable=False),
        sa.Column("expires_at", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("jti"),
    )
    op.create_index(op.f("ix_token_blacklist_jti"), "token_blacklist", ["jti"], unique=False)

    op.add_column(
        "events",
        sa.Column(
            "category",
            sa.String(length=80),
            server_default="improper_clothing",
            nullable=False,
        ),
    )
    op.alter_column("events", "category", server_default=None)


def downgrade() -> None:
    op.drop_column("events", "category")
    op.drop_index(op.f("ix_token_blacklist_jti"), table_name="token_blacklist")
    op.drop_table("token_blacklist")
    op.drop_index(op.f("ix_alert_categories_code"), table_name="alert_categories")
    op.drop_table("alert_categories")
