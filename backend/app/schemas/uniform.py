from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UniformTemplateResponse(BaseModel):
    id: str
    farm_id: str
    name: str
    description: str
    image_paths: list[str]
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class UniformTemplateCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(default="", max_length=500)
    image_paths: list[str] = Field(default_factory=list)
    farm_id: Optional[str] = Field(default=None, max_length=20)


class UniformTemplateUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    image_paths: Optional[list[str]] = None
    required_uniform_id: Optional[str] = None


class UniformUsageZone(BaseModel):
    id: str
    name: str


class UniformUsageResponse(BaseModel):
    in_use: bool
    zones: list[UniformUsageZone] = Field(default_factory=list)
