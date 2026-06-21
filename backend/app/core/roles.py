from __future__ import annotations

SUPER_ADMIN = "SUPER_ADMIN"
FARM_ADMIN = "FARM_ADMIN"
VIEWER = "VIEWER"

ALL_ROLES = (SUPER_ADMIN, FARM_ADMIN, VIEWER)

ROLE_ALIASES = {
    "admin": SUPER_ADMIN,
    "ADMIN": SUPER_ADMIN,
    "super_admin": SUPER_ADMIN,
    "farm_admin": FARM_ADMIN,
    "viewer": VIEWER,
}

DEFAULT_FARM_ID = "FARM-001"

PERMISSIONS: dict[str, set[str]] = {
    SUPER_ADMIN: {"*"},
    FARM_ADMIN: {
        "farm.read",
        "farm.manage_own",
        "camera.read",
        "camera.manage",
        "zone.read",
        "zone.manage",
        "workflow.read",
        "workflow.manage",
        "uniform.read",
        "uniform.manage",
        "settings.read",
        "settings.write",
        "audit.read",
        "backup.read",
        "backup.write",
        "users.read",
        "users.manage_own_farm",
    },
    VIEWER: {
        "farm.read",
        "camera.read",
        "zone.read",
        "workflow.read",
        "uniform.read",
        "settings.read",
        "audit.read",
    },
}


def normalize_role(role: str | None) -> str:
    if not role:
        return VIEWER
    return ROLE_ALIASES.get(role, role)


def role_has_permission(role: str, permission: str) -> bool:
    normalized = normalize_role(role)
    allowed = PERMISSIONS.get(normalized, set())
    return "*" in allowed or permission in allowed
