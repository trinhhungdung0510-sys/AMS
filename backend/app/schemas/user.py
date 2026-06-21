from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    farm_id: str
    is_active: bool


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=6, max_length=128)
    role: str = Field(default="VIEWER", max_length=60)
    farm_id: str = Field(default="FARM-001", max_length=20)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    role: Optional[str] = Field(default=None, max_length=60)
    farm_id: Optional[str] = Field(default=None, max_length=20)
    is_active: Optional[bool] = None
    password: Optional[str] = Field(default=None, min_length=6, max_length=128)
