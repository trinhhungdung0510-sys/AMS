import uuid
from datetime import datetime, timezone

from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.farm_access import assert_can_manage_farm, assert_farm_access, is_super_admin, resolve_farm_scope
from app.core.permissions import require_permission
from app.core.roles import FARM_ADMIN, SUPER_ADMIN, normalize_role
from app.core.security import hash_password
from app.database.session import get_db
from app.models import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.audit import write_audit_log

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)])


def _to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=normalize_role(user.role),
        farm_id=user.farm_id,
        is_active=user.is_active,
    )


@router.get("", response_model=list[UserResponse])
def list_users(
    farm_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.read")),
) -> list[UserResponse]:
    scope = resolve_farm_scope(current_user, farm_id)
    query = select(User).order_by(User.id)
    if scope:
        query = query.where(User.farm_id == scope)
    return [_to_response(user) for user in db.scalars(query)]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.manage_own_farm")),
) -> UserResponse:
    role = normalize_role(payload.role)
    if role == SUPER_ADMIN and not is_super_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không thể tạo SUPER_ADMIN")

    target_farm = payload.farm_id
    if not is_super_admin(current_user):
        target_farm = current_user.farm_id
        if role not in {FARM_ADMIN, "VIEWER"}:
            role = "VIEWER"

    assert_farm_access(current_user, target_farm)

    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email đã tồn tại")

    user = User(
        id=f"USR-{uuid.uuid4().hex[:8].upper()}",
        email=payload.email,
        full_name=payload.full_name,
        role=role,
        farm_id=target_farm,
        hashed_password=hash_password(payload.password),
        is_active=True,
    )
    db.add(user)
    write_audit_log(
        db,
        user_id=current_user.id,
        action="create_user",
        resource_type="user",
        resource_id=user.id,
        farm_id=target_farm,
        metadata={"email": user.email, "role": role},
    )
    db.commit()
    db.refresh(user)
    return _to_response(user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.manage_own_farm")),
) -> UserResponse:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy user")

    assert_farm_access(current_user, user.farm_id)
    values = payload.model_dump(exclude_unset=True)

    if "role" in values:
        values["role"] = normalize_role(values["role"])
        if values["role"] == SUPER_ADMIN and not is_super_admin(current_user):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không thể gán SUPER_ADMIN")

    if "farm_id" in values and not is_super_admin(current_user):
        values.pop("farm_id")

    if "password" in values:
        user.hashed_password = hash_password(values.pop("password"))

    for field, value in values.items():
        setattr(user, field, value)

    write_audit_log(
        db,
        user_id=current_user.id,
        action="update_user",
        resource_type="user",
        resource_id=user.id,
        farm_id=user.farm_id,
        metadata={"fields": list(values.keys())},
    )
    db.commit()
    db.refresh(user)
    return _to_response(user)
