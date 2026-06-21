from __future__ import annotations

from fastapi import HTTPException, status

from app.core.roles import FARM_ADMIN, SUPER_ADMIN, normalize_role
from app.models import User

DEFAULT_FARM_ID = "FARM-001"


def user_farm_id(user: User) -> str:
    return getattr(user, "farm_id", None) or DEFAULT_FARM_ID


def is_super_admin(user: User) -> bool:
    return normalize_role(user.role) == SUPER_ADMIN


def assert_farm_access(user: User, farm_id: str | None) -> None:
    if is_super_admin(user):
        return
    target = farm_id or DEFAULT_FARM_ID
    if user_farm_id(user) != target:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền truy cập farm này",
        )


def resolve_farm_scope(user: User, requested_farm_id: str | None = None) -> str | None:
    if is_super_admin(user):
        return requested_farm_id
    return user_farm_id(user)


def assert_can_manage_farm(user: User, farm_id: str | None) -> None:
    if is_super_admin(user):
        return
    if normalize_role(user.role) != FARM_ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền quản trị")
    assert_farm_access(user, farm_id)
