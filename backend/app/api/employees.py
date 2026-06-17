import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.data.farm_template import TEMPLATE_ZONE_CODES
from app.database.session import get_db
from app.models import Employee
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["employees"])
settings = get_settings()
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


def _get_employee_or_404(employee_id: str, db: Session) -> Employee:
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


def _validate_assigned_zone(zone_code: str) -> None:
    if zone_code not in TEMPLATE_ZONE_CODES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"assigned_zone must be one of the farm template zone codes",
        )


def _ensure_employee_storage() -> Path:
    storage_dir = Path(settings.employee_storage_dir)
    storage_dir.mkdir(parents=True, exist_ok=True)
    return storage_dir


@router.get("", response_model=list[EmployeeResponse])
def list_employees(
    department: Optional[str] = Query(default=None),
    assigned_zone: Optional[str] = Query(default=None),
    active: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db),
) -> list[Employee]:
    query = select(Employee).order_by(Employee.employee_code, Employee.id)
    if department:
        query = query.where(Employee.department == department)
    if assigned_zone:
        query = query.where(Employee.assigned_zone == assigned_zone)
    if active is not None:
        query = query.where(Employee.active.is_(active))
    return list(db.scalars(query))


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: str, db: Session = Depends(get_db)) -> Employee:
    return _get_employee_or_404(employee_id, db)


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)) -> Employee:
    employee_id = payload.id or f"EMP-{uuid.uuid4().hex[:8].upper()}"
    if db.get(Employee, employee_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee id already exists")

    existing_code = db.scalar(select(Employee).where(Employee.employee_code == payload.employee_code))
    if existing_code:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee code already exists")

    _validate_assigned_zone(payload.assigned_zone)

    employee = Employee(
        id=employee_id,
        employee_code=payload.employee_code,
        full_name=payload.full_name,
        department=payload.department,
        assigned_zone=payload.assigned_zone,
        uniform_color=payload.uniform_color,
        face_image=payload.face_image,
        active=payload.active,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: str,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
) -> Employee:
    employee = _get_employee_or_404(employee_id, db)
    values = payload.model_dump(exclude_unset=True)

    if "employee_code" in values:
        duplicate = db.scalar(
            select(Employee)
            .where(Employee.employee_code == values["employee_code"])
            .where(Employee.id != employee_id)
        )
        if duplicate:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee code already exists")

    if "assigned_zone" in values and values["assigned_zone"] is not None:
        _validate_assigned_zone(values["assigned_zone"])

    for field, value in values.items():
        setattr(employee, field, value)

    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: str, db: Session = Depends(get_db)) -> None:
    employee = _get_employee_or_404(employee_id, db)
    db.delete(employee)
    db.commit()


@router.post("/{employee_id}/face-image", response_model=EmployeeResponse)
async def upload_face_image(
    employee_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> Employee:
    employee = _get_employee_or_404(employee_id, db)

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only JPEG, PNG, or WEBP images are supported",
        )

    extension = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }[file.content_type]
    storage_dir = _ensure_employee_storage()
    filename = f"{employee_id}{extension}"
    destination = storage_dir / filename
    content = await file.read()
    destination.write_bytes(content)

    employee.face_image = f"/storage/employees/{filename}"
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
