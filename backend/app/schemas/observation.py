from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.observation import OBJECT_CLASSES, OBSERVATION_SOURCES
from app.core.observation_schema import DEFAULT_SCHEMA_VERSION, normalize_schema_version


class BboxNormalized(BaseModel):
    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)
    width: float = Field(ge=0, le=1)
    height: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def validate_bounds(self) -> "BboxNormalized":
        if self.x + self.width > 1.0001:
            raise ValueError("bbox vượt quá khung hình (x + width > 1)")
        if self.y + self.height > 1.0001:
            raise ValueError("bbox vượt quá khung hình (y + height > 1)")
        return self


class ObservationObject(BaseModel):
    track_id: str = Field(min_length=1, max_length=64, alias="trackId")
    object_class: str = Field(max_length=20, alias="class")
    confidence: float = Field(ge=0, le=1)
    bbox: BboxNormalized
    attributes: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("object_class")
    @classmethod
    def validate_object_class(cls, value: str) -> str:
        normalized = value.strip().lower()
        allowed = {item.lower() for item in OBJECT_CLASSES}
        if normalized not in allowed:
            allowed_display = ", ".join(sorted(OBJECT_CLASSES))
            raise ValueError(f"class phải là một trong: {allowed_display}")
        return normalized


class ObservationCreate(BaseModel):
    camera_id: str = Field(min_length=1, max_length=20, alias="cameraId")
    timestamp: str = Field(min_length=1, max_length=32)
    source: str = Field(max_length=20)
    frame_width: int = Field(ge=1, alias="frameWidth")
    frame_height: int = Field(ge=1, alias="frameHeight")
    objects: list[ObservationObject] = Field(default_factory=list)
    schema_version: str = Field(default=DEFAULT_SCHEMA_VERSION, alias="schemaVersion", max_length=8)

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: str) -> str:
        return normalize_schema_version(value)

    @field_validator("source")
    @classmethod
    def validate_source(cls, value: str) -> str:
        cleaned = value.strip().upper()
        if cleaned not in OBSERVATION_SOURCES:
            allowed = ", ".join(sorted(OBSERVATION_SOURCES))
            raise ValueError(f"source phải là một trong: {allowed}")
        return cleaned


class ObservationResponse(BaseModel):
    id: str
    camera_id: str
    timestamp: str
    source: str
    frame_width: int
    frame_height: int
    objects: list[dict[str, Any]]
    schema_version: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class EventEngineCreate(BaseModel):
    camera_id: str = Field(min_length=1, max_length=20)
    zone_id: str = Field(min_length=1, max_length=24)
    rule_id: str = Field(min_length=1, max_length=24)
    event_type: str = Field(max_length=40)
    severity: str = Field(max_length=20)
    confidence_score: Optional[float] = Field(default=None, ge=0, le=1)
    observation_id: Optional[str] = Field(default=None, max_length=24)
    event_metadata: Optional[dict[str, Any]] = None
