from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

ALLOWED_ZONE_TYPES = {
    "restricted",
    "clean",
    "dirty",
    "warning",
    "monitoring",
}


class ZonePoint(BaseModel):
    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)


class CameraEditorZoneCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    type: str = Field(default="restricted", max_length=40)
    color: str = Field(default="#ff0000", max_length=20)
    points: list[ZonePoint] = Field(min_length=3)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Tên vùng không được để trống")
        return cleaned

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if cleaned not in ALLOWED_ZONE_TYPES:
            allowed = ", ".join(sorted(ALLOWED_ZONE_TYPES))
            raise ValueError(f"Loại vùng phải là một trong: {allowed}")
        return cleaned

    @field_validator("color")
    @classmethod
    def validate_color(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned.startswith("#") or len(cleaned) not in {4, 7}:
            raise ValueError("Màu phải ở dạng hex (#RGB hoặc #RRGGBB)")
        return cleaned


class CameraEditorZoneUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    type: Optional[str] = Field(default=None, max_length=40)
    color: Optional[str] = Field(default=None, max_length=20)
    points: Optional[list[ZonePoint]] = Field(default=None, min_length=3)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Tên vùng không được để trống")
        return cleaned

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        cleaned = value.strip().lower()
        if cleaned not in ALLOWED_ZONE_TYPES:
            allowed = ", ".join(sorted(ALLOWED_ZONE_TYPES))
            raise ValueError(f"Loại vùng phải là một trong: {allowed}")
        return cleaned

    @field_validator("color")
    @classmethod
    def validate_color(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned.startswith("#") or len(cleaned) not in {4, 7}:
            raise ValueError("Màu phải ở dạng hex (#RGB hoặc #RRGGBB)")
        return cleaned


class CameraEditorZoneResponse(BaseModel):
    id: str
    camera_id: str
    name: str
    type: str
    color: str
    points: list[ZonePoint]
    created_at: str

    model_config = ConfigDict(from_attributes=True)
