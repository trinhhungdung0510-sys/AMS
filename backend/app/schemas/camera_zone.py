from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ALLOWED_CAMERA_ZONE_TYPES = {
    "restricted",
    "clean",
    "dirty",
    "warning",
    "monitoring",
    "entry",
    "transition",
}

POINTS_FORMAT_PIXEL = "pixel"
POINTS_FORMAT_NORMALIZED = "normalized"


class ZonePoint(BaseModel):
    x: float = Field(ge=0.0)
    y: float = Field(ge=0.0)


class ZonePointNormalized(BaseModel):
    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)


class CameraZoneCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    parent_zone_id: Optional[str] = Field(default=None, max_length=24)
    description: Optional[str] = Field(default=None, max_length=500)
    type: str = Field(default="monitoring", max_length=40)
    color: str = Field(default="#ff0000", max_length=20)
    points: list[ZonePoint] = Field(min_length=3)
    reference_width: Optional[int] = Field(default=None, ge=1)
    reference_height: Optional[int] = Field(default=None, ge=1)

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
        if cleaned not in ALLOWED_CAMERA_ZONE_TYPES:
            allowed = ", ".join(sorted(ALLOWED_CAMERA_ZONE_TYPES))
            raise ValueError(f"Loại vùng phải là một trong: {allowed}")
        return cleaned

    @field_validator("color")
    @classmethod
    def validate_color(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned.startswith("#") or len(cleaned) not in {4, 7}:
            raise ValueError("Màu phải ở dạng hex (#RGB hoặc #RRGGBB)")
        return cleaned

    @model_validator(mode="after")
    def validate_points_and_reference(self) -> "CameraZoneCreate":
        normalized_input = all(point.x <= 1.0 and point.y <= 1.0 for point in self.points)
        if normalized_input:
            if not self.reference_width or not self.reference_height:
                raise ValueError("reference_width và reference_height bắt buộc khi points chuẩn hóa")
        return self


class CameraZoneUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    parent_zone_id: Optional[str] = Field(default=None, max_length=24)
    description: Optional[str] = Field(default=None, max_length=500)
    type: Optional[str] = Field(default=None, max_length=40)
    color: Optional[str] = Field(default=None, max_length=20)
    points: Optional[list[ZonePoint]] = Field(default=None, min_length=3)
    reference_width: Optional[int] = Field(default=None, ge=1)
    reference_height: Optional[int] = Field(default=None, ge=1)

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
        if cleaned not in ALLOWED_CAMERA_ZONE_TYPES:
            allowed = ", ".join(sorted(ALLOWED_CAMERA_ZONE_TYPES))
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


class CameraZoneResponse(BaseModel):
    id: str
    camera_id: str
    parent_zone_id: Optional[str]
    name: str
    description: Optional[str]
    type: str
    color: str
    points: list[ZonePointNormalized]
    reference_width: Optional[int]
    reference_height: Optional[int]
    points_format: str
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)
