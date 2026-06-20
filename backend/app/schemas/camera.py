from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class CameraBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    manufacturer: Optional[str] = Field(default=None, max_length=120)
    ip: str = Field(min_length=7, max_length=45)
    port: int = Field(default=554, ge=1, le=65535)
    username: str = Field(min_length=1, max_length=120)
    rtsp_url: Optional[str] = Field(default=None, max_length=500)
    status: str = Field(default="online", max_length=20)
    fps: int = Field(default=25, ge=0, le=120)
    resolution: str = Field(default="1080p", max_length=20)
    farm_id: str = Field(default="FARM-001", max_length=20)
    zone: str = Field(default="Chưa phân vùng", max_length=80)
    uptime: float = Field(default=99.0, ge=0, le=100)
    is_active: bool = True

    @field_validator("ip")
    @classmethod
    def validate_ip(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("IP không được để trống")
        return cleaned

    @field_validator("name", "username")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Trường bắt buộc không được để trống")
        return cleaned


class CameraCreate(CameraBase):
    password: str = Field(min_length=1, max_length=255)
    id: Optional[str] = Field(default=None, max_length=20)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Mật khẩu không được để trống")
        return cleaned


class CameraUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    manufacturer: Optional[str] = Field(default=None, max_length=120)
    ip: Optional[str] = Field(default=None, min_length=7, max_length=45)
    port: Optional[int] = Field(default=None, ge=1, le=65535)
    username: Optional[str] = Field(default=None, min_length=1, max_length=120)
    password: Optional[str] = Field(default=None, min_length=1, max_length=255)
    rtsp_url: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = Field(default=None, max_length=20)
    fps: Optional[int] = Field(default=None, ge=0, le=120)
    resolution: Optional[str] = Field(default=None, max_length=20)
    farm_id: Optional[str] = Field(default=None, max_length=20)
    zone: Optional[str] = Field(default=None, max_length=80)
    uptime: Optional[float] = Field(default=None, ge=0, le=100)
    is_active: Optional[bool] = None
    last_seen: Optional[str] = Field(default=None, max_length=32)


class CameraConnectionTestRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    rtsp_url: str = Field(alias="rtspUrl", min_length=8, max_length=500)

    @field_validator("rtsp_url")
    @classmethod
    def validate_rtsp_url(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned.lower().startswith("rtsp://"):
            raise ValueError("rtspUrl phải bắt đầu bằng rtsp://")
        return cleaned


class CameraConnectionTestResponse(BaseModel):
    success: bool
    fps: Optional[int] = None
    resolution: Optional[str] = None
    error: Optional[str] = None


class CameraResponse(BaseModel):
    id: str
    name: str
    manufacturer: Optional[str] = None
    ip: str
    ip_address: str
    port: int
    username: str
    rtsp_url: Optional[str] = None
    status: str
    fps: int
    resolution: str
    last_seen: Optional[str] = None
    created_at: str
    farm_id: str
    zone: str
    uptime: float
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def ensure_ip_aliases(cls, data: object) -> object:
        if isinstance(data, dict):
            if "ip_address" not in data and "ip" in data:
                data["ip_address"] = data["ip"]
            if "ip" not in data and "ip_address" in data:
                data["ip"] = data["ip_address"]
        return data
