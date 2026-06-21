from __future__ import annotations

from app.core.roles import (
    FARM_ADMIN,
    SUPER_ADMIN,
    VIEWER,
    normalize_role,
    role_has_permission,
)


def test_normalize_admin_alias():
    assert normalize_role("admin") == SUPER_ADMIN


def test_super_admin_has_all_permissions():
    assert role_has_permission(SUPER_ADMIN, "backup.write")
    assert role_has_permission(SUPER_ADMIN, "users.manage_own_farm")


def test_viewer_read_only():
    assert role_has_permission(VIEWER, "camera.read")
    assert not role_has_permission(VIEWER, "camera.manage")


def test_farm_admin_manage_scope():
    assert role_has_permission(FARM_ADMIN, "workflow.manage")
    assert role_has_permission(FARM_ADMIN, "uniform.manage")
    assert role_has_permission(FARM_ADMIN, "backup.read")
    assert role_has_permission(FARM_ADMIN, "backup.write")
