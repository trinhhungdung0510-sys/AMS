from pydantic import BaseModel, ConfigDict, Field, field_validator

ALLOWED_DETECTION_LABELS = {
    "person",
    "dog",
    "pig",
    "vehicle",
}


class DetectionBBox(BaseModel):
    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)
    w: float = Field(gt=0.0, le=1.0)
    h: float = Field(gt=0.0, le=1.0)

    @field_validator("w", "h")
    @classmethod
    def validate_size(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Kích thước bbox phải lớn hơn 0")
        return value


class AiDetectionCreate(BaseModel):
    label: str = Field(min_length=1, max_length=40)
    confidence: float = Field(ge=0.0, le=1.0)
    bbox: DetectionBBox

    @field_validator("label")
    @classmethod
    def validate_label(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if cleaned not in ALLOWED_DETECTION_LABELS:
            allowed = ", ".join(sorted(ALLOWED_DETECTION_LABELS))
            raise ValueError(f"Nhãn phải là một trong: {allowed}")
        return cleaned


class AiDetectionResponse(BaseModel):
    id: str
    camera_id: str
    label: str
    confidence: float
    bbox: DetectionBBox
    created_at: str

    model_config = ConfigDict(from_attributes=True)
