"""Danh mục tiếng Việt chuẩn AMS v2.6."""

SEVERITY_LABELS = {
    "CRITICAL": "Nghiêm trọng",
    "WARNING": "Cảnh báo",
    "INFO": "Thông tin",
    "critical": "Nghiêm trọng",
    "danger": "Nghiêm trọng",
    "high": "Mức cao",
    "medium": "Cảnh báo",
    "warning": "Cảnh báo",
    "low": "Thông tin",
    "info": "Thông tin",
}

SEVERITY_EMAIL_PREFIX = {
    "critical": "NGHIÊM TRỌNG",
    "danger": "NGHIÊM TRỌNG",
    "high": "MỨC CAO",
    "medium": "CẢNH BÁO",
    "warning": "CẢNH BÁO",
    "low": "THÔNG TIN",
    "info": "THÔNG TIN",
}

CATEGORY_LABELS = {
    "human": "Con người",
    "animal": "Động vật",
    "vehicle": "Xe cộ",
    "movement": "Di chuyển",
    "contact": "Tiếp xúc",
    "pig": "Heo",
}

ZONE_LEVEL_LABELS = {
    "red": "Khu tuyệt đối cấm",
    "orange": "Khu hạn chế",
    "yellow": "Khu kiểm soát",
    "green": "Khu an toàn",
}

ZONE_LEVEL_COLORS = {
    "red": "#dc2626",
    "orange": "#f97316",
    "yellow": "#eab308",
    "green": "#16a34a",
}

# (zone_code, ten_vung, zone_level, zone_category)
DEFAULT_ZONE_TEMPLATE_VI = [
    ("farm_gate", "Cổng trại", "orange", "perimeter"),
    ("guard_house", "Nhà bảo vệ", "orange", "perimeter"),
    ("shower_room", "Nhà tắm sát trùng", "yellow", "sanitation"),
    ("cafeteria", "Nhà ăn ca", "orange", "facility"),
    ("worker_housing", "Nhà ở công nhân", "orange", "facility"),
    ("feed_storage", "Kho cám", "red", "storage"),
    ("vet_medicine_storage", "Kho thuốc", "red", "storage"),
    ("supply_storage", "Kho vật tư", "yellow", "storage"),
    ("quarantine_barn", "Khu cách ly", "red", "isolation"),
    ("boar_barn", "Khu đực giống", "red", "production"),
    ("gestation_barn", "Khu nái bầu", "red", "production"),
    ("farrowing_barn", "Khu nái đẻ", "red", "production"),
    ("weaning_barn", "Khu cai sữa", "red", "production"),
    ("fattening_barn", "Khu heo thịt", "red", "production"),
    ("pig_loading_zone", "Khu xuất bán", "orange", "perimeter"),
    ("vehicle_disinfection_zone", "Khu sát trùng xe", "yellow", "sanitation"),
    ("parking_zone", "Bãi đỗ xe", "orange", "perimeter"),
    ("internal_road", "Đường nội bộ", "green", "movement"),
]

ZONE_CODE_TO_NAME = {code: name for code, name, _, _ in DEFAULT_ZONE_TEMPLATE_VI}

# Bổ sung alias từ template cũ
ZONE_CODE_TO_NAME.update(
    {
        "person_disinfection_zone": "Khu sát trùng người",
        "handwash_zone": "Khu rửa tay",
        "boot_disinfection_tray": "Khay sát trùng ủng",
        "reception_zone": "Khu tiếp khách",
        "restricted_zone": "Vùng cấm",
        "safe_zone": "Khu an toàn",
        "dirty_zone": "Khu bẩn",
        "disinfection_zone": "Khu sát trùng",
        "production_zone": "Khu sản xuất",
        "outside_zone": "Khu ngoài trại",
        "loading_zone": "Khu xuất nhập",
        "shower_zone": "Nhà tắm sát trùng",
        "feed_storage_zone": "Kho cám",
        "quarantine_zone": "Khu cách ly",
    }
)

BIOSECURITY_LEVEL_TO_ZONE_LEVEL = {
    "restricted": "red",
    "critical": "red",
    "clean": "green",
    "neutral": "yellow",
    "dirty": "orange",
    "low": "green",
    "high": "orange",
    "warning": "yellow",
}

STATUS_LABELS = {
    "new": "Mới",
    "processing": "Đang xử lý",
    "resolved": "Đã xử lý",
}

# (id, rule_code, rule_name_vi, rule_name_en, category, severity, description, enabled)
DEFAULT_BIOSECURITY_RULES_VN = [
    ("BR-VN-001", "PERSON_RESTRICTED_ZONE", "Người xâm nhập vùng cấm", "Person enters restricted zone", "human", "critical", "Phát hiện người đi vào khu vực ATSH bị hạn chế hoặc cấm tuyệt đối.", True),
    ("BR-VN-002", "PERSON_QUARANTINE_INTRUSION", "Người xâm nhập khu cách ly", "Person enters quarantine zone", "human", "critical", "Phát hiện người xâm nhập khu cách ly trái quy định.", True),
    ("BR-VN-003", "ANIMAL_INTRUSION_DOG", "Chó xâm nhập khu chăn nuôi", "Dog enters production area", "animal", "critical", "Phát hiện chó xâm nhập khu chuồng heo hoặc khu sản xuất.", True),
    ("BR-VN-004", "ANIMAL_INTRUSION_CAT", "Mèo xâm nhập khu chăn nuôi", "Cat enters production area", "animal", "high", "Phát hiện mèo xâm nhập khu chuồng heo hoặc khu sản xuất.", True),
    ("BR-VN-005", "ANIMAL_INTRUSION_RAT", "Chuột xuất hiện trong khu vực sản xuất", "Rat detected in production area", "animal", "critical", "Phát hiện chuột trong khu vực sản xuất.", True),
    ("BR-VN-006", "ANIMAL_INTRUSION_BIRD", "Chim xuất hiện trong kho cám", "Bird detected in feed storage", "animal", "medium", "Phát hiện chim trong kho cám hoặc khu thức ăn.", True),
    ("BR-VN-007", "SKIP_SHOWER", "Không tắm sát trùng", "Skipped mandatory shower", "human", "critical", "Công nhân bỏ qua bước tắm sát trùng trước khi vào khu sạch.", True),
    ("BR-VN-008", "SKIP_HAND_DISINFECTION", "Không sát trùng tay", "Skipped hand disinfection", "human", "critical", "Công nhân không thực hiện sát trùng tay tại khu rửa tay.", True),
    ("BR-VN-009", "SKIP_BOOT_DISINFECTION", "Không sát trùng ủng", "Skipped boot disinfection", "human", "critical", "Công nhân bỏ qua khay sát trùng ủng trước khi vào khu sản xuất.", True),
    ("BR-VN-010", "NO_BOOTS", "Không mang ủng bảo hộ", "Missing protective boots", "human", "high", "Phát hiện người không mang ủng bảo hộ trong khu ATSH.", True),
    ("BR-VN-011", "WRONG_UNIFORM_COLOR", "Sai màu quần áo bảo hộ", "Wrong protective uniform color", "human", "medium", "Phát hiện công nhân mặc sai màu quần áo so với khu vực được phép.", True),
    ("BR-VN-012", "DIRTY_TO_CLEAN", "Di chuyển từ vùng bẩn sang vùng sạch", "Dirty zone to clean zone movement", "movement", "critical", "Phát hiện di chuyển trực tiếp từ khu bẩn sang khu sạch mà không qua quy trình ATSH.", True),
    ("BR-VN-013", "VISITOR_CONTACT_WORKER", "Công nhân tiếp xúc người ngoài", "Worker contacts external visitor", "contact", "high", "Phát hiện công nhân tiếp xúc trực tiếp với người ngoài trong khu trại.", True),
    ("BR-VN-014", "DRIVER_CONTACT_WORKER", "Công nhân tiếp xúc lái xe", "Worker contacts vehicle driver", "contact", "high", "Phát hiện công nhân tiếp xúc trực tiếp với lái xe tại khu vực ATSH.", True),
    ("BR-VN-015", "VEHICLE_NO_DISINFECTION", "Xe chưa sát trùng", "Vehicle without disinfection", "vehicle", "critical", "Phát hiện xe vào khu trại mà chưa qua khu sát trùng xe.", True),
    ("BR-VN-016", "VEHICLE_SHORT_DISINFECTION", "Xe sát trùng không đủ thời gian", "Vehicle disinfection time too short", "vehicle", "high", "Phát hiện xe rời khu sát trùng trước thời gian quy định.", True),
    ("BR-VN-017", "VEHICLE_WRONG_PARKING", "Xe đỗ sai vị trí", "Vehicle parked in wrong area", "vehicle", "medium", "Phát hiện xe đỗ ngoài vị trí quy định trong khu trại.", True),
    ("BR-VN-018", "FEED_TRUCK_WRONG_ZONE", "Xe chở cám vào sai khu vực", "Feed truck enters wrong zone", "vehicle", "high", "Phát hiện xe chở cám vào sai khu vực quy định.", True),
    ("BR-VN-019", "PIG_RETURN_TO_BARN", "Heo từ khu xuất bán quay lại khu nuôi", "Pig returns from loading to barn", "pig", "critical", "Phát hiện heo quay lại khu nuôi sau khi đã vào khu xuất bán.", True),
    ("BR-VN-020", "BOAR_BARN_INTRUSION", "Xâm nhập khu đực giống", "Unauthorized boar barn entry", "movement", "critical", "Phát hiện xâm nhập khu đực giống trái quy trình ATSH.", True),
    ("BR-VN-021", "FARROWING_BARN_INTRUSION", "Xâm nhập khu nái đẻ", "Unauthorized farrowing barn entry", "movement", "critical", "Phát hiện xâm nhập khu nái đẻ trái quy trình ATSH.", True),
    ("BR-VN-022", "GESTATION_BARN_INTRUSION", "Xâm nhập khu nái bầu", "Unauthorized gestation barn entry", "movement", "critical", "Phát hiện xâm nhập khu nái bầu trái quy trình ATSH.", True),
    ("BR-VN-023", "WEANING_BARN_INTRUSION", "Xâm nhập khu cai sữa", "Unauthorized weaning barn entry", "movement", "critical", "Phát hiện xâm nhập khu cai sữa trái quy trình ATSH.", True),
    ("BR-VN-024", "FATTENING_BARN_INTRUSION", "Xâm nhập khu heo thịt", "Unauthorized fattening barn entry", "movement", "critical", "Phát hiện xâm nhập khu heo thịt trái quy trình ATSH.", True),
    ("BR-VN-025", "VET_MEDICINE_STORAGE_INTRUSION", "Xâm nhập kho thuốc", "Unauthorized vet medicine storage entry", "movement", "critical", "Phát hiện xâm nhập kho thuốc trái quy định.", True),
    ("BR-VN-026", "SUPPLY_STORAGE_INTRUSION", "Xâm nhập kho vật tư", "Unauthorized supply storage entry", "movement", "high", "Phát hiện xâm nhập kho vật tư trái quy định.", True),
    ("BR-VN-027", "FEED_STORAGE_INTRUSION", "Xâm nhập kho cám", "Unauthorized feed storage entry", "movement", "critical", "Phát hiện xâm nhập kho cám trái quy định.", True),
]

EMAIL_FIELD_LABELS = {
    "farm": "Trang trại",
    "camera": "Camera",
    "zone": "Khu vực",
    "violation_type": "Loại vi phạm",
    "object": "Đối tượng",
    "confidence": "Độ tin cậy AI",
    "time": "Thời gian",
    "snapshot": "Ảnh vi phạm",
}
