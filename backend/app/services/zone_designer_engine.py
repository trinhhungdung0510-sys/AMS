from typing import Optional

from app.data.zone_designer_catalog import (
    ATSH_LEVEL_COLORS,
    ATSH_LEVEL_LABELS,
    DEFAULT_ATSH_BY_TYPE,
    ZONE_TYPE_CODES,
    ZONE_TYPE_LABELS,
)
from app.models import ZonePolygon


def validate_zone_type(zone_type: str) -> None:
    if zone_type not in ZONE_TYPE_CODES:
        raise ValueError(f"Loại vùng không hỗ trợ: {zone_type}")


def validate_biosecurity_level(level: str) -> None:
    if level not in ATSH_LEVEL_LABELS:
        raise ValueError(f"Mức ATSH không hợp lệ: {level}")


def resolve_color(*, biosecurity_level: str, color: Optional[str] = None) -> str:
    if color:
        return color
    return ATSH_LEVEL_COLORS.get(biosecurity_level, ATSH_LEVEL_COLORS["yellow"])


def resolve_default_level(zone_type: str, biosecurity_level: Optional[str] = None) -> str:
    if biosecurity_level:
        return biosecurity_level
    return DEFAULT_ATSH_BY_TYPE.get(zone_type, "yellow")


def zone_to_response_dict(zone: ZonePolygon) -> dict:
    level = zone.biosecurity_level or DEFAULT_ATSH_BY_TYPE.get(zone.zone_type, "yellow")
    return {
        "id": zone.id,
        "ten_vung": zone.zone_name,
        "ten_loai_vung": ZONE_TYPE_LABELS.get(zone.zone_type, zone.zone_type),
        "ma_vung": zone.zone_type,
        "cap_atsh": level,
        "muc_atsh": ATSH_LEVEL_LABELS.get(level, level),
        "mau_sac": zone.color,
        "do_mo": zone.opacity if zone.opacity is not None else 0.3,
        "mo_ta": zone.description or "",
        "camera_id": zone.camera_id,
        "trang_trai_id": zone.farm_id,
        "diem_polygon": zone.polygon_points,
        "dang_hoat_dong": zone.active,
        "thoi_gian_tao": zone.created_at,
    }
