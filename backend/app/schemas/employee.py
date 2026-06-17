from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EmployeeBase(BaseModel):
    employee_code: str = Field(min_length=2, max_length=40)
    full_name: str = Field(min_length=2, max_length=120)
    department: str = Field(min_length=2, max_length=80)
    assigned_zone: str = Field(min_length=2, max_length=40)
    uniform_color: str = Field(min_length=2, max_length=40)
    face_image: str = ""
    active: bool = True


class EmployeeCreate(EmployeeBase):
    id: Optional[str] = None


class EmployeeUpdate(BaseModel):
    employee_code: Optional[str] = Field(default=None, min_length=2, max_length=40)
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    department: Optional[str] = Field(default=None, min_length=2, max_length=80)
    assigned_zone: Optional[str] = Field(default=None, min_length=2, max_length=40)
    uniform_color: Optional[str] = Field(default=None, min_length=2, max_length=40)
    face_image: Optional[str] = None
    active: Optional[bool] = None


class EmployeeResponse(EmployeeBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
