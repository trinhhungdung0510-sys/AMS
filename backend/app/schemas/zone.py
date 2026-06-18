from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.data.zone_designer_catalog import (
    ATSH_LEVEL_COLORS,
    ATSH_LEVEL_LABELS,
    DEFAULT_ATSH_BY_TYPE,
    ZONE_DESIGNER_TYPES,
    ZONE_TYPE_CODES,
    ZONE_TYPE_LABELS,
)

ZONE_TYPES = ZONE_TYPE_CODES


class ZonePolygonBase(BaseModel):
    farm_id: str
    camera_id: str
    zone_name: str = Field(min_length=1, max_length=120)
    zone_type: str = Field(min_length=1, max_length=40)
    biosecurity_level: str = Field(default="yellow", max_length=20)
    color: Optional[str] = None
    opacity: float = Field(default=0.3, ge=0.05, le=1.0)
    description: str = Field(default="", max_length=500)
    polygon_points: list[list[float]] = Field(min_length=3)
    active: bool = True


class ZonePolygonCreate(ZonePolygonBase):
    id: Optional[str] = None


class ZonePolygonUpdate(BaseModel):
    farm_id: Optional[str] = None
    camera_id: Optional[str] = None
    zone_name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    zone_type: Optional[str] = Field(default=None, min_length=1, max_length=40)
    biosecurity_level: Optional[str] = Field(default=None, max_length=20)
    color: Optional[str] = None
    opacity: Optional[float] = Field(default=None, ge=0.05, le=1.0)
    description: Optional[str] = Field(default=None, max_length=500)
    polygon_points: Optional[list[list[float]]] = Field(default=None, min_length=3)
    active: Optional[bool] = None


class ZonePolygonResponse(BaseModel):
    id: str
    ten_vung: str
    ten_loai_vung: str
    ma_vung: str
    cap_atsh: str
    muc_atsh: str
    mau_sac: str
    do_mo: float
    mo_ta: str
    camera_id: str
    trang_trai_id: str
    diem_polygon: list[list[float]]
    dang_hoat_dong: bool
    thoi_gian_tao: str

    model_config = ConfigDict(from_attributes=True)


class ZoneClassificationResponse(BaseModel):
    cap_do: str
    ten: str
    mau_sac: str


class ZoneTypeOptionResponse(BaseModel):
    ma_vung: str
    ten_loai_vung: str
    cap_atsh_mac_dinh: str
    muc_atsh: str
    mau_sac: str


class ZoneTemplateItemResponse(BaseModel):
    ma_vung: str
    ten_vung: str
    phan_loai_vung: str
