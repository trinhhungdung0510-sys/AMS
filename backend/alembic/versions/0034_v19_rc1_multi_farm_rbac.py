"""AMS v1.9 RC1 multi-farm, RBAC, system settings.

Revision ID: 0034_v19_rc1
Revises: 0033_compliance_uniform_v17
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0034_v19_rc1"
down_revision = "0033_compliance_uniform_v17"
branch_labels = None
depends_on = None

DEFAULT_FARM_ID = "FARM-001"


def upgrade() -> None:
    op.add_column("farms", sa.Column("code", sa.String(length=40), nullable=True))
    op.add_column("farms", sa.Column("address", sa.String(length=255), nullable=True))
    op.add_column("farms", sa.Column("contact_name", sa.String(length=120), nullable=True))
    op.add_column("farms", sa.Column("contact_phone", sa.String(length=40), nullable=True))
    op.add_column("farms", sa.Column("created_at", sa.String(length=32), nullable=True))

    op.execute(
        sa.text(
            """
            UPDATE farms
            SET code = id,
                address = location,
                created_at = COALESCE(created_at, NOW()::text)
            WHERE code IS NULL
            """
        )
    )

    op.add_column(
        "users",
        sa.Column("farm_id", sa.String(length=20), server_default=DEFAULT_FARM_ID, nullable=False),
    )
    op.add_column(
        "workflows",
        sa.Column("farm_id", sa.String(length=20), server_default=DEFAULT_FARM_ID, nullable=False),
    )
    op.add_column(
        "uniform_templates",
        sa.Column("farm_id", sa.String(length=20), server_default=DEFAULT_FARM_ID, nullable=False),
    )
    op.add_column(
        "camera_zones",
        sa.Column("farm_id", sa.String(length=20), server_default=DEFAULT_FARM_ID, nullable=False),
    )
    op.add_column("audit_logs", sa.Column("farm_id", sa.String(length=20), nullable=True))

    op.create_table(
        "system_settings",
        sa.Column("key", sa.String(length=80), primary_key=True),
        sa.Column("value_json", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.String(length=32), nullable=False),
        sa.Column("updated_by", sa.String(length=20), nullable=True),
    )

    op.execute(
        sa.text(
            """
            UPDATE users SET role = 'SUPER_ADMIN' WHERE role IN ('admin', 'ADMIN', 'super_admin')
            """
        )
    )


def downgrade() -> None:
    op.drop_table("system_settings")
    op.drop_column("audit_logs", "farm_id")
    op.drop_column("camera_zones", "farm_id")
    op.drop_column("uniform_templates", "farm_id")
    op.drop_column("workflows", "farm_id")
    op.drop_column("users", "farm_id")
    op.drop_column("farms", "created_at")
    op.drop_column("farms", "contact_phone")
    op.drop_column("farms", "contact_name")
    op.drop_column("farms", "address")
    op.drop_column("farms", "code")
