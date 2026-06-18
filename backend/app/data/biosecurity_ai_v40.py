"""AMS v4.0 Biosecurity AI Engine — ATSH rules, severities, farm area types."""

ATSH_SEVERITY_LEVELS = {
    "INFO": "Thông tin",
    "WARNING": "Cảnh báo",
    "CRITICAL": "Nghiêm trọng",
}

LEGACY_SEVERITY_TO_ATSH = {
    "info": "INFO",
    "low": "INFO",
    "warning": "WARNING",
    "medium": "WARNING",
    "high": "WARNING",
    "danger": "CRITICAL",
    "critical": "CRITICAL",
}

# (zone_code, ten_vi, ten_en, cap_atsh)
FARM_AREA_TYPES = [
    ("quarantine_barn", "Chuồng cách ly", "Isolation Barn", "CRITICAL"),
    ("gestation_barn", "Chuồng nái bầu", "Gestation Barn", "CRITICAL"),
    ("farrowing_barn", "Chuồng nái đẻ", "Farrowing Barn", "CRITICAL"),
    ("boar_barn", "Chuồng đực giống", "Boar Barn", "CRITICAL"),
    ("weaning_barn", "Chuồng cai sữa", "Nursery Barn", "CRITICAL"),
    ("fattening_barn", "Chuồng heo thịt", "Finisher Barn", "CRITICAL"),
    ("worker_housing", "Nhà ở công nhân", "Worker House", "WARNING"),
    ("shower_room", "Nhà tắm", "Shower Room", "WARNING"),
    ("cafeteria", "Nhà ăn", "Canteen", "WARNING"),
    ("feed_storage", "Kho cám", "Feed Warehouse", "CRITICAL"),
    ("vet_medicine_storage", "Kho thuốc", "Medicine Warehouse", "CRITICAL"),
    ("supply_storage", "Kho vật tư", "Supply Warehouse", "WARNING"),
    ("farm_gate", "Cổng trại", "Security Gate", "WARNING"),
]

FARM_AREA_CODES = {item[0] for item in FARM_AREA_TYPES}
FARM_AREA_LABELS_VI = {code: label for code, label, _, _ in FARM_AREA_TYPES}
FARM_AREA_LABELS_EN = {code: label for code, _, label, _ in FARM_AREA_TYPES}

CLEAN_BIOSECURITY_LEVELS = {"clean", "green"}
DIRTY_BIOSECURITY_LEVELS = {"dirty", "orange"}
RESTRICTED_BIOSECURITY_LEVELS = {"restricted", "red", "critical"}

SANITATION_ZONE_CODES = {
    "shower_room",
    "handwash_zone",
    "person_disinfection_zone",
    "vehicle_disinfection_zone",
    "boot_disinfection_tray",
}

PRODUCTION_BARN_CODES = {
    "quarantine_barn",
    "gestation_barn",
    "farrowing_barn",
    "boar_barn",
    "weaning_barn",
    "fattening_barn",
}

PIG_TRUCK_ZONES = {"pig_loading_zone", "vehicle_disinfection_zone"}
FEED_TRUCK_ZONES = {"feed_storage", "parking_zone"}
PIG_TRUCK_OBJECT_TYPES = {"pig_truck", "vehicle", "truck"}
FEED_TRUCK_OBJECT_TYPES = {"feed_truck", "vehicle", "truck"}

# id, rule_code, rule_name_vi, rule_name_en, category, severity, description, rule_type, evaluation_mode, object_type
V4_ATSH_RULES = [
    (
        "BR-V4-001",
        "FORBIDDEN_ZONE_INTRUSION",
        "Xâm nhập vùng cấm",
        "Forbidden Zone Intrusion",
        "human",
        "CRITICAL",
        "Phát hiện người hoặc đối tượng xâm nhập khu vực ATSH bị cấm.",
        "forbidden_zone_intrusion",
        "zone_entry",
        "person",
    ),
    (
        "BR-V4-002",
        "ANIMAL_INTRUSION_CLEAN_ZONE",
        "Động vật xâm nhập khu sạch",
        "Animal Intrusion Into Clean Zone",
        "animal",
        "CRITICAL",
        "Phát hiện động vật lạ xâm nhập khu vực sạch hoặc chuồng heo.",
        "animal_intrusion_clean_zone",
        "zone_entry",
        "animal",
    ),
    (
        "BR-V4-003",
        "DIRTY_TO_CLEAN_MOVEMENT",
        "Di chuyển từ vùng bẩn sang vùng sạch",
        "Dirty Zone To Clean Zone Movement",
        "movement",
        "CRITICAL",
        "Phát hiện di chuyển trực tiếp từ khu bẩn sang khu sạch mà không qua ATSH.",
        "dirty_to_clean_movement",
        "zone_transition",
        "person",
    ),
    (
        "BR-V4-004",
        "WORKER_CONTACT_PIG_TRUCK",
        "Công nhân tiếp xúc xe heo",
        "Worker Contact Pig Truck",
        "contact",
        "WARNING",
        "Phát hiện công nhân tiếp xúc xe vận chuyển heo tại khu xuất nhập.",
        "worker_contact_pig_truck",
        "contact",
        "person",
    ),
    (
        "BR-V4-005",
        "WORKER_CONTACT_FEED_TRUCK",
        "Công nhân tiếp xúc xe cám",
        "Worker Contact Feed Truck",
        "contact",
        "WARNING",
        "Phát hiện công nhân tiếp xúc xe vận chuyển cám tại khu kho cám.",
        "worker_contact_feed_truck",
        "contact",
        "person",
    ),
]

AI_CATEGORY_TO_ATSH_RULE = {
    "restricted_zone_intrusion": "FORBIDDEN_ZONE_INTRUSION",
    "animal_intrusion": "ANIMAL_INTRUSION_CLEAN_ZONE",
    "dirty_to_clean": "DIRTY_TO_CLEAN_MOVEMENT",
    "worker_pig_truck_contact": "WORKER_CONTACT_PIG_TRUCK",
    "worker_feed_truck_contact": "WORKER_CONTACT_FEED_TRUCK",
}


def normalize_atsh_severity(severity: str) -> str:
    key = (severity or "WARNING").strip()
    upper = key.upper()
    if upper in ATSH_SEVERITY_LEVELS:
        return upper
    return LEGACY_SEVERITY_TO_ATSH.get(key.lower(), "WARNING")
