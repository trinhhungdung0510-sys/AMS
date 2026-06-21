from app.api.deps import get_current_user
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.farm_access import resolve_farm_scope
from app.core.permissions import require_permission
from app.database.session import get_db
from app.models import AuditLog, User
from app.schemas.audit import AuditLogResponse

router = APIRouter(prefix="/audit", tags=["audit"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[AuditLogResponse])
def list_audit_logs(
    farm_id: Optional[str] = Query(default=None),
    action: Optional[str] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("audit.read")),
) -> list[AuditLog]:
    scope = resolve_farm_scope(current_user, farm_id)
    query = select(AuditLog).order_by(AuditLog.created_at.desc(), AuditLog.id).limit(limit)
    if scope:
        query = query.where(AuditLog.farm_id == scope)
    if action:
        query = query.where(AuditLog.action == action)
    return list(db.scalars(query))
