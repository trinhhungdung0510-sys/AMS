import uuid
from datetime import datetime, timezone

from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.farm_access import assert_farm_access, resolve_farm_scope
from app.core.permissions import require_permission
from app.database.session import get_db
from app.models import UniformTemplate, User
from app.schemas.uniform import (
    UniformTemplateCreate,
    UniformTemplateResponse,
    UniformTemplateUpdate,
    UniformUsageResponse,
)
from app.services.audit import write_audit_log
from app.services.uniform_service import delete_uniform_template, get_uniform_usage

router = APIRouter(prefix="/uniforms", tags=["uniforms"], dependencies=[Depends(get_current_user)])


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _to_response(item: UniformTemplate) -> UniformTemplateResponse:
    return UniformTemplateResponse.model_validate(item)


@router.get("", response_model=list[UniformTemplateResponse])
def list_uniforms(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("uniform.read")),
) -> list[UniformTemplateResponse]:
    scope = resolve_farm_scope(current_user)
    query = select(UniformTemplate).order_by(UniformTemplate.id)
    if scope:
        query = query.where(UniformTemplate.farm_id == scope)
    return [_to_response(item) for item in db.scalars(query)]


@router.post("", response_model=UniformTemplateResponse, status_code=status.HTTP_201_CREATED)
def create_uniform(
    payload: UniformTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("uniform.manage")),
) -> UniformTemplateResponse:
    farm_id = payload.farm_id or current_user.farm_id
    assert_farm_access(current_user, farm_id)
    now = utc_now_iso()
    item = UniformTemplate(
        id=f"UNI-{uuid.uuid4().hex[:8].upper()}",
        farm_id=farm_id,
        name=payload.name,
        description=payload.description,
        image_paths=payload.image_paths,
        created_at=now,
        updated_at=now,
    )
    db.add(item)
    write_audit_log(
        db,
        user_id=current_user.id,
        action="create_uniform",
        resource_type="uniform_template",
        resource_id=item.id,
        farm_id=farm_id,
        metadata={"name": item.name},
    )
    db.commit()
    db.refresh(item)
    return _to_response(item)


@router.get("/{uniform_id}/usage", response_model=UniformUsageResponse)
def uniform_usage(
    uniform_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("uniform.read")),
) -> UniformUsageResponse:
    item = db.get(UniformTemplate, uniform_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy uniform")

    assert_farm_access(current_user, item.farm_id)
    return UniformUsageResponse.model_validate(get_uniform_usage(db, uniform_id))


@router.put("/{uniform_id}", response_model=UniformTemplateResponse)
def update_uniform(
    uniform_id: str,
    payload: UniformTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("uniform.manage")),
) -> UniformTemplateResponse:
    item = db.get(UniformTemplate, uniform_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy uniform")

    assert_farm_access(current_user, item.farm_id)
    values = payload.model_dump(exclude_unset=True)
    for field, value in values.items():
        setattr(item, field, value)
    item.updated_at = utc_now_iso()

    db.commit()
    db.refresh(item)
    return _to_response(item)


@router.delete("/{uniform_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_uniform(
    uniform_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("uniform.manage")),
) -> None:
    item = db.get(UniformTemplate, uniform_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy uniform")

    assert_farm_access(current_user, item.farm_id)
    uniform_name = item.name
    farm_id = item.farm_id

    delete_uniform_template(db, item)
    write_audit_log(
        db,
        user_id=current_user.id,
        action="delete_uniform",
        resource_type="uniform_template",
        resource_id=uniform_id,
        farm_id=farm_id,
        metadata={"name": uniform_name},
    )
    db.commit()
