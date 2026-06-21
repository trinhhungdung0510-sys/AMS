import json
from datetime import datetime, timezone

from sqlalchemy import select

from app.core.security import hash_password
from app.data.workflow_defaults import DEFAULT_WORKFLOWS, build_workflow_steps
from app.data.animal_intrusion import DEFAULT_ANIMAL_INTRUSION_POLICIES
from app.data.biosecurity_ai_v40 import V4_ATSH_RULES
from app.data.biosecurity_rules_vn import DEFAULT_BIOSECURITY_RULES_VN
from app.data.vi_catalog import DEFAULT_ZONE_TEMPLATE_VI
from app.data.farm_template import (
    DEFAULT_ATSH_RULES,
    STANDARD_PIG_FARM_TEMPLATE,
    TEMPLATE_ZONE_DEFINITIONS,
)
from app.database.session import SessionLocal
from app.models import (
    AIModel,
    AITask,
    AlertCategory,
    AnimalIntrusionPolicy,
    AuditLog,
    BiosecurityRule,
    Camera,
    CameraHealth,
    CameraStream,
    EdgeDevice,
    Employee,
    Event,
    EventSnapshot,
    Farm,
    FarmLayout,
    FarmLayoutTemplate,
    FarmMapLayout,
    FarmMapLayer,
    FarmMapObject,
    FarmObject,
    FarmRoute,
    FarmZone,
    License,
    NotificationGateway,
    NotificationRule,
    TemplateZoneDefinition,
    TrackWorkflowProgress,
    User,
    Visitor,
    Workflow,
    WorkflowStep,
    ZonePolygon,
    ZoneTransition,
)

CAMERAS = [
    ("CAM-001", "FARM-001", "Camera Cổng trại", "Cổng trại", "192.168.10.11", "online", "1080p", 99.8, 30),
    ("CAM-002", "FARM-001", "Camera Khu nái 01", "Khu nái", "192.168.10.12", "online", "2K", 99.3, 25),
    ("CAM-003", "FARM-001", "Camera Khu nái 02", "Khu nái", "192.168.10.13", "online", "1080p", 98.7, 25),
    ("CAM-004", "FARM-001", "Camera Khu đực giống", "Khu đực giống", "192.168.10.14", "online", "1080p", 97.9, 24),
    ("CAM-005", "FARM-001", "Camera Khu cách ly", "Khu cách ly", "192.168.10.15", "offline", "1080p", 82.1, 0),
    ("CAM-006", "FARM-002", "Camera Hành lang chính", "Hành lang chính", "192.168.10.16", "online", "720p", 99.1, 20),
    ("CAM-007", "FARM-002", "Camera Khu con", "Khu con", "192.168.10.17", "online", "1080p", 98.4, 24),
    ("CAM-008", "FARM-002", "Camera Kho thức ăn", "Kho thức ăn", "192.168.10.18", "online", "1080p", 99.6, 25),
    ("CAM-009", "FARM-002", "Camera Bể xử lý nước", "Xử lý nước", "192.168.10.19", "online", "720p", 96.5, 20),
]

ALERT_CATEGORIES = [
    ("improper_clothing", "Người không đúng trang phục", "warning"),
    ("restricted_zone_intrusion", "Người và động vật xâm nhập vùng cấm", "danger"),
    ("pig_fever", "Heo sốt bất thường", "danger"),
    ("pig_abnormal", "Heo nằm bất động kéo dài", "critical"),
    ("vehicle_disinfection", "Xe chưa qua khử trùng", "warning"),
    ("camera_offline", "Camera mất kết nối", "critical"),
    ("animal_intrusion", "Động vật xâm nhập vùng cấm", "danger"),
    ("workflow_violation", "Vi phạm quy trình ATSH", "critical"),
]

STATUSES = ["new", "processing", "resolved"]
HANDLERS = ["Chưa phân công", "Nguyễn Minh An", "Trần Bảo Long", "Phạm Thu Hà"]

FARM_ZONES = [
    (
        f"FZ-{zone[0].split('-')[1]}",
        "FARM-001",
        STANDARD_PIG_FARM_TEMPLATE["id"],
        zone[0],
        zone[1],
        zone[2],
        zone[3],
        zone[4],
        zone[5],
        zone[7],
        zone[8],
        zone[9],
        zone[10],
        zone[11],
        True,
    )
    for zone in TEMPLATE_ZONE_DEFINITIONS
]

# Bổ sung 18 khu vực chuẩn tiếng Việt (v2.6)
FARM_ZONES_VI = [
    (
        f"FZ-VI-{index:03d}",
        "FARM-001",
        STANDARD_PIG_FARM_TEMPLATE["id"],
        None,
        zone_code,
        zone_name,
        zone_category,
        {"red": "restricted", "orange": "dirty", "yellow": "neutral", "green": "clean"}[zone_level],
        {"red": "critical", "orange": "warning", "yellow": "warning", "green": "low"}[zone_level],
        10.0 + (index % 6) * 12.0,
        10.0 + (index // 6) * 14.0,
        12.0,
        10.0,
        index,
        True,
    )
    for index, (zone_code, zone_name, zone_level, zone_category) in enumerate(DEFAULT_ZONE_TEMPLATE_VI, start=1)
]

FARM_MAP_LAYOUT = (
    "MAP-LAYOUT-001",
    "FARM-001",
    "Bản đồ trang trại chính",
    False,
    True,
    10.9321,
    106.8521,
    17,
    "satellite",
)

FARM_MAP_OBJECTS = [
    ("MAP-001", "MAP-LAYOUT-001", "gate-in", "Cổng vào", "Cổng trại", "", 10.93172, 106.85152, 0.00025, 0.00035, 0, "dirty", "yellow", None, None, None, None, "active"),
    ("MAP-002", "MAP-LAYOUT-001", "pig-quarantine", "Chuồng cách ly heo", "Chuồng cách ly", "", 10.93255, 106.85285, 0.00045, 0.00055, 0, "quarantine", "red", None, None, None, None, "active"),
    ("MAP-003", "MAP-LAYOUT-001", "shower", "Nhà tắm", "Hành lang chính", "", 10.93195, 106.85185, 0.00035, 0.0004, 0, "sanitation", "green", None, None, None, None, "active"),
    ("MAP-004", "MAP-LAYOUT-001", "camera", "Camera Cổng trại", "Cổng trại", "", 10.93175, 106.85155, 0.00008, 0.00008, 45, "clean", "green", "CAM-001", "MAP-001", 90.0, 60.0, "online"),
    ("MAP-005", "MAP-LAYOUT-001", "camera", "Camera Khu nái 01", "Khu nái", "", 10.93235, 106.85215, 0.00008, 0.00008, 0, "clean", "green", "CAM-002", "MAP-006", 135.0, 55.0, "online"),
    ("MAP-006", "MAP-LAYOUT-001", "gestation", "Chuồng nái", "Khu nái", "", 10.9323, 106.8521, 0.0005, 0.0006, 0, "clean", "green", None, None, None, None, "active"),
    ("MAP-007", "MAP-LAYOUT-001", "camera", "Camera Khu cách ly", "Chuồng cách ly", "", 10.93258, 106.85288, 0.00008, 0.00008, 0, "quarantine", "orange", "CAM-005", "MAP-002", 180.0, 60.0, "offline"),
    ("MAP-008", "MAP-LAYOUT-001", "feed", "Kho cám", "Kho cám", "", 10.93185, 106.85135, 0.00035, 0.0004, 0, "dirty", "orange", None, None, None, None, "active"),
    ("MAP-009", "MAP-LAYOUT-001", "camera", "Camera Kho cám", "Kho cám", "", 10.93188, 106.85138, 0.00008, 0.00008, 0, "dirty", "yellow", "CAM-008", "MAP-008", 270.0, 55.0, "online"),
]

SMART_FARM_LAYOUT = (
    "SF-LAYOUT-001",
    "FARM-001",
    "Sơ đồ trang trại AMS",
    "Ấp Bình Minh, Xã Long Thành, Đồng Nai",
    10.9321,
    106.8521,
    17,
    "satellite",
    False,
    True,
)

SMART_FARM_OBJECTS = FARM_MAP_OBJECTS

SMART_FARM_ROUTES = [
    (
        "SF-ROUTE-001",
        "SF-LAYOUT-001",
        "worker",
        "Luồng công nhân",
        '[[10.93195, 106.85185], [10.9321, 106.8520], [10.9323, 106.8521]]',
        '["Nhà tắm", "Sát trùng", "Chuồng nái"]',
        True,
    ),
]

SMART_FARM_LAYERS = [
    ("SF-LAYOUT-001-L1", "SF-LAYOUT-001", "objects", True, 1.0),
    ("SF-LAYOUT-001-L2", "SF-LAYOUT-001", "cameras", True, 1.0),
    ("SF-LAYOUT-001-L3", "SF-LAYOUT-001", "atsh", True, 0.85),
    ("SF-LAYOUT-001-L4", "SF-LAYOUT-001", "routes", True, 1.0),
    ("SF-LAYOUT-001-L5", "SF-LAYOUT-001", "heatmap", False, 0.6),
]

ZONE_POLYGONS = [
    (
        "ZP-GATE-001",
        "FARM-001",
        "CAM-001",
        "Cổng trại",
        "farm_gate",
        "orange",
        "#f97316",
        [[40, 40], [360, 40], [360, 220], [40, 220]],
        True,
    ),
    (
        "ZP-GATE-002",
        "FARM-001",
        "CAM-001",
        "Bãi đỗ xe",
        "parking_zone",
        "orange",
        "#f97316",
        [[390, 40], [720, 40], [720, 240], [390, 240]],
        True,
    ),
    (
        "ZP-GATE-003",
        "FARM-001",
        "CAM-001",
        "Khu sát trùng người",
        "person_disinfection_zone",
        "yellow",
        "#eab308",
        [[750, 60], [1180, 60], [1180, 360], [750, 360]],
        True,
    ),
    (
        "ZP-GATE-004",
        "FARM-001",
        "CAM-001",
        "Khu sát trùng xe",
        "vehicle_disinfection_zone",
        "yellow",
        "#eab308",
        [[430, 280], [720, 280], [760, 500], [390, 500]],
        True,
    ),
    (
        "ZP-GATE-005",
        "FARM-001",
        "CAM-001",
        "Khay sát trùng ủng",
        "boot_disinfection_tray",
        "yellow",
        "#eab308",
        [[80, 280], [300, 280], [300, 460], [80, 460]],
        True,
    ),
    (
        "ZP-GATE-006",
        "FARM-001",
        "CAM-001",
        "Chuồng nái bầu",
        "gestation_barn",
        "red",
        "#dc2626",
        [[820, 380], [1120, 380], [1120, 620], [820, 620]],
        True,
    ),
]

ZONE_TRANSITIONS = [
    ("ZT-SEED-001", "person", 501, "CAM-001", "parking_zone", "gestation_barn", "2026-06-17T18:20:00+07:00"),
    ("ZT-SEED-002", "vehicle", 502, "CAM-001", "parking_zone", "pig_loading_zone", "2026-06-17T18:21:00+07:00"),
    ("ZT-SEED-003", "dog", 503, "CAM-001", "reception_zone", "farrowing_barn", "2026-06-17T18:22:00+07:00"),
    ("ZT-SEED-004", "person", 504, "CAM-001", "parking_zone", "person_disinfection_zone", "2026-06-17T18:19:00+07:00"),
    ("ZT-SEED-005", "person", 504, "CAM-001", "person_disinfection_zone", "gestation_barn", "2026-06-17T18:19:30+07:00"),
    ("ZT-SEED-006", "person", 601, "CAM-001", "reception_zone", "parking_zone", "2026-06-17T19:00:00+07:00"),
    ("ZT-SEED-007", "person", 601, "CAM-001", "parking_zone", "vehicle_disinfection_zone", "2026-06-17T19:01:00+07:00"),
    ("ZT-SEED-008", "vehicle", 602, "CAM-001", "parking_zone", "vehicle_disinfection_zone", "2026-06-17T19:02:00+07:00"),
]

BIOSECURITY_RULES = DEFAULT_ATSH_RULES
SEED_CREATED_AT = "2026-06-17T00:00:00+07:00"


def _atsh_rule_category(object_type: str) -> str:
    if object_type in {"dog", "cat", "rat", "bird"}:
        return "animal"
    if object_type == "vehicle":
        return "vehicle"
    if object_type == "person":
        return "human"
    return "movement"

EMPLOYEES = [
    ("EMP-001", "NV-001", "Nguyễn Văn An", "Sản xuất", "gestation_barn", "xanh lá", "", True),
    ("EMP-002", "NV-002", "Trần Thị Bình", "Sản xuất", "farrowing_barn", "xanh lá", "", True),
    ("EMP-003", "NV-003", "Lê Hoàng Cường", "An ninh", "guard_house", "xám", "", True),
    ("EMP-004", "NV-004", "Phạm Minh Dũng", "Thú y", "vet_medicine_storage", "trắng", "", True),
    ("EMP-005", "NV-005", "Võ Thị Em", "Kho vận", "feed_storage", "cam", "", True),
    ("EMP-006", "NV-006", "Hoàng Văn Phúc", "Hành chính", "reception_zone", "xanh dương", "", True),
    ("EMP-007", "NV-007", "Đặng Thị Giang", "Sản xuất", "weaning_barn", "xanh lá", "", True),
    ("EMP-008", "NV-008", "Bùi Quốc Huy", "Sản xuất", "boar_barn", "xanh lá", "", False),
]

VISITORS = [
    (
        "VIS-001",
        "Nguyễn Thanh Tùng",
        "Công ty CP Thức ăn Chăn nuôi",
        "51A-12345",
        "Kiểm tra quy trình cho ăn",
        "2026-06-17T08:30:00+07:00",
        "2026-06-17T11:00:00+07:00",
        "Nguyễn Minh An",
    ),
    (
        "VIS-002",
        "Trần Quốc Bảo",
        "Sở NN&PTNT Long An",
        "51B-67890",
        "Thanh tra ATSH định kỳ",
        "2026-06-17T09:00:00+07:00",
        None,
        "AMS Administrator",
    ),
    (
        "VIS-003",
        "Lê Thị Hồng",
        "Công ty Thiết bị chăn nuôi ABC",
        "",
        "Bảo trì hệ thống camera",
        None,
        None,
        "Trần Bảo Long",
    ),
    (
        "VIS-004",
        "Phạm Văn Đức",
        "Đại lý thuốc thú y VetPro",
        "51C-11223",
        "Giao thuốc kháng sinh",
        "2026-06-17T13:15:00+07:00",
        None,
        "Phạm Thu Hà",
    ),
]

FARMS = [
    ("FARM-001", "AMS Farm Long An", "Long An, Việt Nam", "enterprise", "active"),
    ("FARM-002", "AMS Farm Đồng Nai", "Đồng Nai, Việt Nam", "professional", "active"),
]

EDGE_DEVICES = [
    ("EDGE-001", "FARM-001", "AI Box Cổng trại", "NVIDIA Jetson Orin", "AMS-EDGE-001", "online", 5),
    ("EDGE-002", "FARM-002", "AI Box Khu chuồng", "NVIDIA Jetson Xavier", "AMS-EDGE-002", "online", 4),
]

NOTIFICATION_GATEWAYS = [
    ("GW-001", "FARM-001", "telegram", "@ams_farm_longan_alerts", True, "online"),
    ("GW-002", "FARM-001", "email", "ops-longan@ams.local", True, "online"),
    ("GW-003", "FARM-002", "webhook", "https://hooks.ams.local/dongnai", True, "online"),
]

LICENSES = [
    ("LIC-001", "FARM-001", "enterprise", 64, 12, "2026-01-01", "2026-12-31", "active"),
    ("LIC-002", "FARM-002", "professional", 32, 8, "2026-03-01", "2027-02-28", "active"),
]

AI_MODELS = [
    ("AIM-001", "AMS PPE Detector", "improper_clothing", "1.2.0", True),
    ("AIM-002", "AMS Restricted Zone Intrusion", "restricted_zone_intrusion", "1.2.0", True),
    ("AIM-003", "AMS Pig Fever Thermal", "pig_fever", "1.1.3", True),
    ("AIM-004", "AMS Pig Abnormal Behavior", "pig_abnormal", "1.0.8", True),
    ("AIM-005", "AMS Vehicle Disinfection Check", "vehicle_disinfection", "1.0.2", True),
    ("AIM-006", "AMS Camera Health Monitor", "camera_offline", "1.2.0", True),
]

def seed() -> None:
    db = SessionLocal()
    try:
        for farm in FARMS:
            db.merge(
                Farm(
                    id=farm[0],
                    name=farm[1],
                    location=farm[2],
                    plan=farm[3],
                    status=farm[4],
                )
            )

        for camera in CAMERAS:
            ip = camera[4]
            is_online = camera[5] == "online"
            now = datetime.now(timezone.utc).isoformat()
            db.merge(
                Camera(
                    id=camera[0],
                    farm_id=camera[1],
                    name=camera[2],
                    zone=camera[3],
                    manufacturer="Hikvision",
                    ip=ip,
                    port=554,
                    username="admin",
                    password="admin123",
                    rtsp_url=f"rtsp://admin:admin123@{ip}:554/Streaming/Channels/101",
                    status=camera[5],
                    resolution=camera[6],
                    uptime=camera[7],
                    fps=camera[8],
                    is_active=True,
                    last_seen=now if is_online else None,
                    created_at=now,
                )
            )

        db.merge(
            FarmLayoutTemplate(
                id=STANDARD_PIG_FARM_TEMPLATE["id"],
                name=STANDARD_PIG_FARM_TEMPLATE["name"],
                description=STANDARD_PIG_FARM_TEMPLATE["description"],
                version=STANDARD_PIG_FARM_TEMPLATE["version"],
            )
        )

        for zone in TEMPLATE_ZONE_DEFINITIONS:
            db.merge(
                TemplateZoneDefinition(
                    id=zone[0],
                    template_id=STANDARD_PIG_FARM_TEMPLATE["id"],
                    zone_code=zone[1],
                    zone_name=zone[2],
                    zone_category=zone[3],
                    biosecurity_level=zone[4],
                    risk_level=zone[5],
                    color=zone[6],
                    layout_x=zone[7],
                    layout_y=zone[8],
                    layout_w=zone[9],
                    layout_h=zone[10],
                    sort_order=zone[11],
                )
            )

        for zone in FARM_ZONES:
            db.merge(
                FarmZone(
                    id=zone[0],
                    farm_id=zone[1],
                    template_id=zone[2],
                    template_zone_id=zone[3],
                    zone_code=zone[4],
                    name=zone[5],
                    zone_category=zone[6],
                    biosecurity_level=zone[7],
                    risk_level=zone[8],
                    layout_x=zone[9],
                    layout_y=zone[10],
                    layout_w=zone[11],
                    layout_h=zone[12],
                    sort_order=zone[13],
                    active=zone[14],
                )
            )

        for zone in FARM_ZONES_VI:
            db.merge(
                FarmZone(
                    id=zone[0],
                    farm_id=zone[1],
                    template_id=zone[2],
                    template_zone_id=zone[3],
                    zone_code=zone[4],
                    name=zone[5],
                    zone_category=zone[6],
                    biosecurity_level=zone[7],
                    risk_level=zone[8],
                    layout_x=zone[9],
                    layout_y=zone[10],
                    layout_w=zone[11],
                    layout_h=zone[12],
                    sort_order=zone[13],
                    active=zone[14],
                )
            )

        for category in ALERT_CATEGORIES:
            db.merge(
                AlertCategory(
                    code=category[0],
                    label=category[1],
                    severity=category[2],
                )
            )

        for model in AI_MODELS:
            db.merge(
                AIModel(
                    id=model[0],
                    model_name=model[1],
                    model_type=model[2],
                    version=model[3],
                    enabled=model[4],
                )
            )

        for camera in CAMERAS:
            db.merge(
                CameraStream(
                    id=f"STR-{camera[0].split('-')[1]}",
                    camera_id=camera[0],
                    rtsp_url=f"rtsp://ams:demo@{camera[4]}:554/live",
                    fps=camera[8],
                    resolution=camera[6],
                    stream_status="offline" if camera[5] == "offline" else "live",
                )
            )
            db.merge(
                CameraHealth(
                    id=f"HLT-{camera[0].split('-')[1]}",
                    farm_id=camera[1],
                    camera_id=camera[0],
                    fps=camera[8],
                    bitrate=4.2 if camera[6] == "1080p" else 6.8 if camera[6] == "2K" else 2.6,
                    last_seen="2026-06-17T17:10:00+07:00",
                    status="offline" if camera[5] == "offline" else "healthy",
                )
            )

        for device in EDGE_DEVICES:
            db.merge(
                EdgeDevice(
                    id=device[0],
                    farm_id=device[1],
                    device_name=device[2],
                    device_type=device[3],
                    serial_number=device[4],
                    status=device[5],
                    assigned_cameras=device[6],
                )
            )

        for gateway in NOTIFICATION_GATEWAYS:
            db.merge(
                NotificationGateway(
                    id=gateway[0],
                    farm_id=gateway[1],
                    gateway_type=gateway[2],
                    endpoint=gateway[3],
                    enabled=gateway[4],
                    status=gateway[5],
                )
            )

        for license_item in LICENSES:
            db.merge(
                License(
                    id=license_item[0],
                    farm_id=license_item[1],
                    plan=license_item[2],
                    max_cameras=license_item[3],
                    max_ai_models=license_item[4],
                    start_date=license_item[5],
                    end_date=license_item[6],
                    status=license_item[7],
                )
            )

        for map_object in FARM_MAP_OBJECTS:
            db.merge(
                FarmMapObject(
                    id=map_object[0],
                    layout_id=map_object[1],
                    object_type=map_object[2],
                    name=map_object[3],
                    zone=map_object[4],
                    description=map_object[5],
                    x=map_object[6],
                    y=map_object[7],
                    width=map_object[8],
                    height=map_object[9],
                    rotation=map_object[10],
                    atsh_zone_type=map_object[11],
                    atsh_level=map_object[12],
                    linked_camera_id=map_object[13],
                    linked_zone_id=map_object[14],
                    camera_direction=map_object[15],
                    camera_fov=map_object[16],
                    status=map_object[17],
                )
            )

        db.merge(
            FarmMapLayout(
                id=FARM_MAP_LAYOUT[0],
                farm_id=FARM_MAP_LAYOUT[1],
                name=FARM_MAP_LAYOUT[2],
                is_template=FARM_MAP_LAYOUT[3],
                is_active=FARM_MAP_LAYOUT[4],
                center_lat=FARM_MAP_LAYOUT[5],
                center_lng=FARM_MAP_LAYOUT[6],
                zoom=FARM_MAP_LAYOUT[7],
                base_layer=FARM_MAP_LAYOUT[8],
            )
        )

        db.merge(
            FarmLayout(
                id=SMART_FARM_LAYOUT[0],
                farm_id=SMART_FARM_LAYOUT[1],
                name=SMART_FARM_LAYOUT[2],
                address=SMART_FARM_LAYOUT[3],
                center_lat=SMART_FARM_LAYOUT[4],
                center_lng=SMART_FARM_LAYOUT[5],
                zoom=SMART_FARM_LAYOUT[6],
                base_layer=SMART_FARM_LAYOUT[7],
                is_template=SMART_FARM_LAYOUT[8],
                is_active=SMART_FARM_LAYOUT[9],
            )
        )

        for obj in SMART_FARM_OBJECTS:
            db.merge(
                FarmObject(
                    id=obj[0],
                    layout_id=SMART_FARM_LAYOUT[0],
                    object_type=obj[2],
                    name=obj[3],
                    description=obj[5],
                    x=obj[6],
                    y=obj[7],
                    width=obj[8],
                    height=obj[9],
                    rotation=obj[10],
                    atsh_zone_type=obj[11],
                    atsh_level=obj[12],
                    linked_camera_id=obj[13],
                    linked_zone_id=obj[14],
                    camera_direction=obj[15],
                    camera_fov=obj[16],
                    status=obj[17],
                )
            )

        for route in SMART_FARM_ROUTES:
            db.merge(
                FarmRoute(
                    id=route[0],
                    layout_id=route[1],
                    route_type=route[2],
                    name=route[3],
                    points=route[4],
                    labels=route[5],
                    valid=route[6],
                )
            )

        for layer in SMART_FARM_LAYERS:
            db.merge(
                FarmMapLayer(
                    id=layer[0],
                    layout_id=layer[1],
                    layer_key=layer[2],
                    visible=layer[3],
                    opacity=layer[4],
                )
            )

        for zone_polygon in ZONE_POLYGONS:
            db.merge(
                ZonePolygon(
                    id=zone_polygon[0],
                    farm_id=zone_polygon[1],
                    camera_id=zone_polygon[2],
                    zone_name=zone_polygon[3],
                    zone_type=zone_polygon[4],
                    biosecurity_level=zone_polygon[5],
                    color=zone_polygon[6],
                    opacity=0.3,
                    description="",
                    polygon_points=zone_polygon[7],
                    active=zone_polygon[8],
                    created_at="2026-06-17T18:17:00+07:00",
                )
            )

        for transition in ZONE_TRANSITIONS:
            db.merge(
                ZoneTransition(
                    id=transition[0],
                    object_type=transition[1],
                    track_id=transition[2],
                    camera_id=transition[3],
                    from_zone=transition[4],
                    to_zone=transition[5],
                    cross_time=transition[6],
                    timestamp=transition[6],
                )
            )

        for legacy_rule_id in ("BR-001", "BR-002", "BR-003", "BR-004", "BR-005"):
            legacy_rule = db.get(BiosecurityRule, legacy_rule_id)
            if legacy_rule:
                db.delete(legacy_rule)

        for old_rule in list(db.scalars(select(BiosecurityRule).where(BiosecurityRule.id.like("BR-VN-%")))):
            db.delete(old_rule)
        db.flush()

        for rule in V4_ATSH_RULES:
            db.merge(
                BiosecurityRule(
                    id=rule[0],
                    rule_code=rule[1],
                    rule_name_vi=rule[2],
                    rule_name_en=rule[3],
                    category=rule[4],
                    severity=rule[5].lower(),
                    description=rule[6],
                    enabled=True,
                    created_at=SEED_CREATED_AT,
                    object_type=rule[9],
                    from_zone=None,
                    to_zone=None,
                    required_zone=None,
                    rule_type=rule[7],
                    evaluation_mode=rule[8],
                )
            )

        for rule in DEFAULT_BIOSECURITY_RULES_VN:
            db.merge(
                BiosecurityRule(
                    id=rule[0],
                    rule_code=rule[1],
                    rule_name_vi=rule[2],
                    rule_name_en=rule[3],
                    category=rule[4],
                    severity=rule[5],
                    description=rule[6],
                    enabled=rule[7],
                    created_at=SEED_CREATED_AT,
                    object_type="catalog",
                    from_zone=None,
                    to_zone=None,
                    required_zone=None,
                )
            )

        for rule in BIOSECURITY_RULES:
            db.merge(
                BiosecurityRule(
                    id=rule[0],
                    rule_code=rule[2].upper(),
                    rule_name_vi=rule[1],
                    rule_name_en=rule[1],
                    category=_atsh_rule_category(rule[3]),
                    severity=rule[7],
                    description=rule[1],
                    enabled=rule[8],
                    created_at=SEED_CREATED_AT,
                    object_type=rule[3],
                    from_zone=rule[4],
                    to_zone=rule[5],
                    required_zone=rule[6],
                )
            )

        for employee in EMPLOYEES:
            db.merge(
                Employee(
                    id=employee[0],
                    employee_code=employee[1],
                    full_name=employee[2],
                    department=employee[3],
                    assigned_zone=employee[4],
                    uniform_color=employee[5],
                    face_image=employee[6],
                    active=employee[7],
                )
            )

        for visitor in VISITORS:
            db.merge(
                Visitor(
                    id=visitor[0],
                    visitor_name=visitor[1],
                    company=visitor[2],
                    vehicle_plate=visitor[3],
                    visit_purpose=visitor[4],
                    arrival_time=visitor[5],
                    departure_time=visitor[6],
                    approved_by=visitor[7],
                )
            )

        for policy in DEFAULT_ANIMAL_INTRUSION_POLICIES:
            db.merge(
                AnimalIntrusionPolicy(
                    id=policy["id"],
                    object_type=policy["object_type"],
                    allowed_zones=policy["allowed_zones"],
                    restricted_zones=policy["restricted_zones"],
                    severity=policy["severity"],
                    enabled=policy["enabled"],
                )
            )

        seed_timestamp = datetime.now(timezone.utc).isoformat()
        legacy_workflow_ids = ["WF-PERSON-ENTRY"]
        for legacy_id in legacy_workflow_ids:
            legacy_steps = list(db.scalars(select(WorkflowStep).where(WorkflowStep.workflow_id == legacy_id)))
            for step in legacy_steps:
                db.delete(step)
            legacy = db.get(Workflow, legacy_id)
            if legacy:
                db.delete(legacy)
        db.flush()

        for workflow_def in DEFAULT_WORKFLOWS:
            db.merge(
                Workflow(
                    id=workflow_def["id"],
                    name=workflow_def["name"],
                    description=workflow_def["description"],
                    object_type=workflow_def["object_type"],
                    enabled=workflow_def["enabled"],
                    created_at=seed_timestamp,
                )
            )
            for step in build_workflow_steps(workflow_def["id"], workflow_def["final_step"]):
                db.merge(
                    WorkflowStep(
                        id=step[0],
                        workflow_id=workflow_def["id"],
                        step_order=step[1],
                        step_name=step[2],
                        zone_code=step[3],
                        required=True,
                    )
                )

        for category in ALERT_CATEGORIES:
            db.merge(
                NotificationRule(
                    id=f"NR-{ALERT_CATEGORIES.index(category) + 1:03d}",
                    name=f"Thông báo {category[1]}",
                    alert_category=category[0],
                    severity=category[2],
                    email=True,
                    telegram=category[2] in {"danger", "critical"},
                    zalo=category[0] in {"pig_fever", "pig_abnormal"},
                    enabled=True,
                )
            )

        db.merge(
            User(
                id="USR-ADMIN",
                email="admin@ams.local",
                full_name="AMS Administrator",
                role="SUPER_ADMIN",
                farm_id="FARM-001",
                hashed_password=hash_password("admin123"),
                is_active=True,
            )
        )

        for index in range(50):
            camera = CAMERAS[index % len(CAMERAS)]
            category = ALERT_CATEGORIES[index % len(ALERT_CATEGORIES)]
            day = 17 - (index % 10)
            hour = 6 + ((index * 3) % 17)
            minute = (index * 11) % 60
            status = STATUSES[index % len(STATUSES)]

            db.merge(
                Event(
                    id=f"EVT-{index + 1:03d}",
                    farm_id=camera[1],
                    camera_id=camera[0],
                    category=category[0],
                    alert_type=category[1],
                    zone=camera[3],
                    severity=category[2],
                    status=status,
                    handler="Chưa phân công" if status == "new" else HANDLERS[index % len(HANDLERS)],
                    confidence=min(99, 82 + ((index * 7) % 18)),
                    occurred_at=f"2026-06-{day:02d}T{hour:02d}:{minute:02d}:00+07:00",
                )
            )

        for index in range(20):
            event_id = f"EVT-{index + 1:03d}"
            db.merge(
                EventSnapshot(
                    id=f"SNP-{index + 1:03d}",
                    event_id=event_id,
                    image_path=f"/storage/snapshots/{event_id}.jpg",
                    thumbnail_path=f"/storage/snapshots/thumbs/{event_id}.jpg",
                )
            )

        for index in range(12):
            camera = CAMERAS[index % len(CAMERAS)]
            category = ALERT_CATEGORIES[index % len(ALERT_CATEGORIES)]
            db.merge(
                AITask(
                    id=f"TASK-SEED-{index + 1:03d}",
                    camera_id=camera[0],
                    category=category[0],
                    status="completed" if index < 8 else "queued",
                    priority=10 - (index % 6),
                    result=json.dumps(
                        {
                            "source": "seed",
                            "confidence": min(99, 84 + index),
                            "event_id": f"EVT-{index + 1:03d}" if index < 8 else None,
                        },
                        ensure_ascii=False,
                    ),
                    created_at=f"2026-06-17T{8 + index:02d}:00:00+07:00",
                    processed_at=f"2026-06-17T{8 + index:02d}:00:05+07:00" if index < 8 else None,
                )
            )

        now = datetime.now(timezone.utc).isoformat()
        for index, action in enumerate(["login", "logout", "create_camera", "update_notification_rule"]):
            db.merge(
                AuditLog(
                    id=f"AUD-SEED-{index + 1:03d}",
                    user_id="USR-ADMIN",
                    action=action,
                    resource_type="system",
                    resource_id=f"SEED-{index + 1:03d}",
                    metadata_json=json.dumps({"source": "seed"}, ensure_ascii=False),
                    created_at=now,
                )
            )

        db.commit()
        print(
            "Seeded v4.0 Employee Management data: 2 farms, 1 admin, 9 cameras, 9 health rows, "
            "2 edge devices, 3 notification gateways, 2 licenses, 9 streams, "
            "6 AI models, 50 AI events, 20 snapshots, 1 farm template, 20 template zones, "
            "20 farm zones, 9 map objects, 6 zone polygons, 8 zone transitions, "
            f"{len(V4_ATSH_RULES)} quy tắc ATSH v4.0, {len(DEFAULT_BIOSECURITY_RULES_VN)} quy tắc ATSH VN, {len(BIOSECURITY_RULES)} quy tắc vận hành, "
            f"{len(EMPLOYEES)} employees, {len(VISITORS)} visitors, 6 notification rules, 12 AI tasks, 4 audit logs."
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
