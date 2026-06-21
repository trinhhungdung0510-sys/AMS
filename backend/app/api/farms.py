import uuid
from datetime import datetime, timezone

from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.farm_access import assert_can_manage_farm, assert_farm_access, is_super_admin, resolve_farm_scope
from app.core.permissions import require_permission
from app.core.roles import SUPER_ADMIN
from app.database.session import get_db
from app.models import Farm, User
from app.schemas.farm import FarmCreate, FarmResponse, FarmUpdate
from app.services.audit import write_audit_log

router = APIRouter(prefix="/farms", tags=["farms"], dependencies=[Depends(get_current_user)])


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def farm_to_response(farm: Farm) -> FarmResponse:
    return FarmResponse(
        id=farm.id,
        name=farm.name,
        code=farm.code or farm.id,
        address=farm.address or farm.location,
        contactName=farm.contact_name,
        contactPhone=farm.contact_phone,
        createdAt=farm.created_at,
        location=farm.location,
        plan=farm.plan,
        status=farm.status,
    )


@router.get("", response_model=list[FarmResponse])
def list_farms(
    farm_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("farm.read")),
) -> list[FarmResponse]:
    scope = resolve_farm_scope(current_user, farm_id)
    query = select(Farm).order_by(Farm.id)
    if scope:
        query = query.where(Farm.id == scope)
    return [farm_to_response(farm) for farm in db.scalars(query)]


@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm(
    farm_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("farm.read")),
) -> FarmResponse:
    assert_farm_access(current_user, farm_id)
    farm = db.get(Farm, farm_id)
    if not farm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy farm")
    return farm_to_response(farm)


@router.post("", response_model=FarmResponse, status_code=status.HTTP_201_CREATED)
def create_farm(
    payload: FarmCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("farm.manage_own")),
) -> FarmResponse:
    if not is_super_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ SUPER_ADMIN được tạo farm")

    if db.get(Farm, payload.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Farm id đã tồn tại")

    farm = Farm(
        id=payload.id,
        name=payload.name,
        code=payload.code or payload.id,
        address=payload.address or payload.location or "",
        contact_name=payload.contactName,
        contact_phone=payload.contactPhone,
        created_at=utc_now_iso(),
        location=payload.location or payload.address or "",
        plan=payload.plan,
        status=payload.status,
    )
    db.add(farm)
    write_audit_log(
        db,
        user_id=current_user.id,
        action="create_farm",
        resource_type="farm",
        resource_id=farm.id,
        farm_id=farm.id,
        metadata={"name": farm.name},
    )
    db.commit()
    db.refresh(farm)
    return farm_to_response(farm)


@router.put("/{farm_id}", response_model=FarmResponse)
def update_farm(
    farm_id: str,
    payload: FarmUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("farm.manage_own")),
) -> FarmResponse:
    assert_can_manage_farm(current_user, farm_id)
    farm = db.get(Farm, farm_id)
    if not farm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy farm")

    values = payload.model_dump(exclude_unset=True)
    mapping = {
        "contactName": "contact_name",
        "contactPhone": "contact_phone",
    }
    for field, value in values.items():
        setattr(farm, mapping.get(field, field), value)

    write_audit_log(
        db,
        user_id=current_user.id,
        action="update_farm",
        resource_type="farm",
        resource_id=farm.id,
        farm_id=farm.id,
        metadata={"fields": list(values.keys())},
    )
    db.commit()
    db.refresh(farm)
    return farm_to_response(farm)
