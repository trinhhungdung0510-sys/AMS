from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.farm_access import assert_can_manage_farm, is_super_admin
from app.core.permissions import require_permission
from app.core.roles import SUPER_ADMIN
from app.database.session import get_db
from app.models import User
from app.schemas.system import (
    BackupRestoreResponse,
    RestoreRequest,
    SystemSettingsResponse,
    SystemSettingsUpdate,
)
from app.services.audit import write_audit_log
from app.services.backup_service import export_backup, restore_backup
from app.services.system_settings_service import get_system_settings, save_system_settings

router = APIRouter(prefix="/system", tags=["system"], dependencies=[Depends(get_current_user)])


@router.get("/settings", response_model=SystemSettingsResponse)
def read_system_settings(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("settings.read")),
) -> SystemSettingsResponse:
    return SystemSettingsResponse(**get_system_settings(db))


@router.put("/settings", response_model=SystemSettingsResponse)
def update_system_settings(
    payload: SystemSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("settings.write")),
) -> SystemSettingsResponse:
    values = payload.model_dump(exclude_unset=True)
    if not is_super_admin(current_user):
        values.pop("demo_mode", None)

    updated = save_system_settings(db, values, updated_by=current_user.id)
    write_audit_log(
        db,
        user_id=current_user.id,
        action="update_settings",
        resource_type="system_settings",
        resource_id="global",
        farm_id=current_user.farm_id,
        metadata=values,
    )
    db.commit()
    return SystemSettingsResponse(**updated)


@router.post("/backup", response_model=BackupRestoreResponse)
def create_backup(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("backup.read")),
) -> BackupRestoreResponse:
    payload = export_backup(db)
    write_audit_log(
        db,
        user_id=current_user.id,
        action="create_backup",
        resource_type="system_backup",
        resource_id="global",
        farm_id=current_user.farm_id,
        metadata={"version": payload["version"]},
    )
    db.commit()
    return BackupRestoreResponse(**payload)


@router.post("/restore")
def restore_configuration(
    payload: RestoreRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("backup.write")),
) -> dict:
    if not is_super_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ SUPER_ADMIN được restore")

    counts = restore_backup(db, payload.model_dump(exclude_none=True))
    write_audit_log(
        db,
        user_id=current_user.id,
        action="restore_backup",
        resource_type="system_backup",
        resource_id="global",
        farm_id=current_user.farm_id,
        metadata=counts,
    )
    db.commit()
    return {"status": "restored", "counts": counts}
