"""Danh mục loại vùng và phân cấp ATSH cho Zone Designer v3.0."""

ATSH_LEVEL_LABELS = {
    "red": "Vùng cấm",
    "orange": "Vùng hạn chế",
    "yellow": "Vùng kiểm soát",
    "green": "Vùng an toàn",
}

ATSH_LEVEL_COLORS = {
    "red": "#dc2626",
    "orange": "#f97316",
    "yellow": "#eab308",
    "green": "#16a34a",
}

# (zone_code, ten_loai_vung, cap_atsh_mac_dinh)
ZONE_DESIGNER_TYPES = [
    ("farm_gate", "Cổng trại", "orange"),
    ("guard_house", "Nhà bảo vệ", "orange"),
    ("shower_room", "Nhà tắm", "yellow"),
    ("handwash_zone", "Khu sát trùng tay", "yellow"),
    ("worker_housing", "Nhà ở công nhân", "orange"),
    ("cafeteria", "Nhà ăn", "orange"),
    ("feed_storage", "Kho cám", "red"),
    ("vet_medicine_storage", "Kho thuốc", "red"),
    ("supply_storage", "Kho vật tư", "yellow"),
    ("quarantine_barn", "Chuồng cách ly", "red"),
    ("boar_barn", "Chuồng đực giống", "red"),
    ("gestation_barn", "Chuồng nái bầu", "red"),
    ("farrowing_barn", "Chuồng nái đẻ", "red"),
    ("weaning_barn", "Chuồng cai sữa", "red"),
    ("fattening_barn", "Chuồng heo thịt", "red"),
    ("pig_loading_zone", "Khu xuất bán", "orange"),
    ("person_disinfection_zone", "Khu sát trùng người", "yellow"),
    ("vehicle_disinfection_zone", "Khu sát trùng xe", "yellow"),
    ("boot_disinfection_tray", "Khay sát trùng ủng", "yellow"),
    ("parking_zone", "Bãi đỗ xe", "orange"),
    ("internal_road", "Đường nội bộ", "green"),
]

ZONE_TYPE_CODES = {item[0] for item in ZONE_DESIGNER_TYPES}
ZONE_TYPE_LABELS = {code: label for code, label, _ in ZONE_DESIGNER_TYPES}
DEFAULT_ATSH_BY_TYPE = {code: level for code, _, level in ZONE_DESIGNER_TYPES}
