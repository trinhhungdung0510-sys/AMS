import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import bearer_scheme, get_current_user
from app.core.redis import get_redis_client
from app.core.security import create_access_token, decode_access_token, verify_password
from app.database.session import get_db
from app.models import TokenBlacklist, User
from app.core.roles import normalize_role
from app.schemas.auth import LoginRequest, LogoutResponse, TokenResponse, UserMeResponse
from app.services.audit import write_audit_log

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email, User.is_active.is_(True)))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token, expires_at, _ = create_access_token(subject=user.id, role=user.role)
    write_audit_log(
        db,
        user_id=user.id,
        action="login",
        resource_type="auth",
        resource_id=user.id,
        farm_id=user.farm_id,
        metadata={"email": user.email},
    )
    db.commit()
    return TokenResponse(
        access_token=token,
        expires_at=expires_at,
        user=UserMeResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=normalize_role(user.role),
            farm_id=user.farm_id,
            is_active=user.is_active,
        ),
    )


@router.post("/logout", response_model=LogoutResponse)
def logout(
    credentials=Depends(bearer_scheme),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LogoutResponse:
    payload = decode_access_token(credentials.credentials)
    if payload:
        jti = payload["jti"]
        expires_at = int(payload["exp"])
        ttl = max(1, expires_at - int(time.time()))

        redis_client = get_redis_client()
        redis_client.setex(f"jwt:blacklist:{jti}", ttl, current_user.id)

        db.merge(TokenBlacklist(jti=jti, user_id=current_user.id, expires_at=expires_at))
        write_audit_log(
            db,
            user_id=current_user.id,
            action="logout",
            resource_type="auth",
            resource_id=current_user.id,
            metadata={"jti": jti},
        )
        db.commit()

    return LogoutResponse(status="logged_out")


@router.get("/me", response_model=UserMeResponse)
def me(current_user: User = Depends(get_current_user)) -> UserMeResponse:
    return UserMeResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=normalize_role(current_user.role),
        farm_id=current_user.farm_id,
        is_active=current_user.is_active,
    )
