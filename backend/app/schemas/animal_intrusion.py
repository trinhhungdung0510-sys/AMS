from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AnimalIntrusionPolicyBase(BaseModel):
    object_type: str = Field(min_length=2, max_length=40)
    allowed_zones: list[str] = Field(default_factory=list)
    restricted_zones: list[str] = Field(default_factory=list)
    severity: str = Field(min_length=3, max_length=20)
    enabled: bool = True


class AnimalIntrusionPolicyCreate(AnimalIntrusionPolicyBase):
    id: Optional[str] = None


class AnimalIntrusionPolicyUpdate(BaseModel):
    allowed_zones: Optional[list[str]] = None
    restricted_zones: Optional[list[str]] = None
    severity: Optional[str] = Field(default=None, min_length=3, max_length=20)
    enabled: Optional[bool] = None


class AnimalIntrusionPolicyResponse(AnimalIntrusionPolicyBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
