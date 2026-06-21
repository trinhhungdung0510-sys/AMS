from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FarmResponse(BaseModel):
    id: str
    name: str
    code: Optional[str] = None
    address: Optional[str] = None
    contactName: Optional[str] = Field(default=None, alias="contact_name")
    contactPhone: Optional[str] = Field(default=None, alias="contact_phone")
    createdAt: Optional[str] = Field(default=None, alias="created_at")
    location: str
    plan: str
    status: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FarmCreate(BaseModel):
    id: str = Field(min_length=2, max_length=20)
    name: str = Field(min_length=2, max_length=120)
    code: Optional[str] = Field(default=None, max_length=40)
    address: Optional[str] = Field(default=None, max_length=255)
    contactName: Optional[str] = Field(default=None, max_length=120)
    contactPhone: Optional[str] = Field(default=None, max_length=40)
    location: Optional[str] = Field(default=None, max_length=160)
    plan: str = Field(default="standard", max_length=40)
    status: str = Field(default="active", max_length=20)


class FarmUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    code: Optional[str] = Field(default=None, max_length=40)
    address: Optional[str] = Field(default=None, max_length=255)
    contactName: Optional[str] = Field(default=None, max_length=120)
    contactPhone: Optional[str] = Field(default=None, max_length=40)
    location: Optional[str] = Field(default=None, max_length=160)
    plan: Optional[str] = Field(default=None, max_length=40)
    status: Optional[str] = Field(default=None, max_length=20)
