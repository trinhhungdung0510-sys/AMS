from __future__ import annotations

from typing import Callable

from fastapi import Depends, HTTPException, status

from app.api.deps import get_current_user
from app.core.roles import normalize_role, role_has_permission
from app.models import User


def require_permission(permission: str) -> Callable:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        role = normalize_role(current_user.role)
        if not role_has_permission(role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {permission}",
            )
        return current_user

    return dependency


def require_roles(*roles: str) -> Callable:
    allowed = {normalize_role(role) for role in roles}

    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if normalize_role(current_user.role) not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return current_user

    return dependency
