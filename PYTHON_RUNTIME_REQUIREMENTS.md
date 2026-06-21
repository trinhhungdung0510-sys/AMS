# Python Runtime Requirements — AMS Backend

**Required Python Version: 3.11+**

AMS backend **không chạy được** trên Python 3.9 trở xuống. Nhiều module import trực tiếp với cú pháp PEP 604 / PEP 585 **không** có `from __future__ import annotations`, nên annotation được evaluate lúc import — gây `TypeError` trên runtime cũ.

Ví dụ lỗi trên Python 3.9:

```text
File "app/api/cameras.py", line 40
    farm_id: str | None = Query(default=None),
TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'
```

---

## Yêu cầu chính thức

| Item | Version |
|------|---------|
| **Python (backend)** | **3.11+** (khuyến nghị 3.11 hoặc 3.12) |
| Node.js (frontend) | 18+ |
| PostgreSQL | 14+ |
| Redis | 6+ |

### Kiểm tra phiên bản

```bash
python3 --version    # Python 3.11.x hoặc 3.12.x
python3.11 --version
```

### Tạo venv đúng phiên bản

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Tổng quan cú pháp Python 3.10+ trong codebase

Quét toàn bộ `backend/app/`, `backend/tests/`, `backend/scripts/`, `backend/alembic/` (2026-06-18):

| Cú pháp | Số lần xuất hiện | Số file | Python tối thiểu |
|---------|------------------|---------|------------------|
| `str \| None` và union `X \| Y` | **146 dòng** | **47 file** | **3.10+** (PEP 604) |
| `list[...]`, `dict[...]`, `tuple[...]`, `set[...]` | **420 dòng** | **129 file** | **3.10+** runtime thực tế |
| `dict[str, Any]` | **137** | **35 file** | PEP 585 |
| `list[str]` | **34** | nhiều file | PEP 585 |
| `Optional[...]` (typing cũ) | **497** | **108 file** | 3.7+ (tương thích) |
| `from __future__ import annotations` | **106 file** | **106 file** | Hoãn evaluate — **không đủ** nếu file thiếu |
| `match` / `case` (structural) | **0** | **0** | **Không dùng** |
| `TypeAlias`, `Self`, `except*`, `tomllib` | **0** | **0** | **Không dùng** |

### Phân loại union types

| Pattern | Occurrences | Files |
|---------|-------------|-------|
| `str \| None` | 85 | 29 |
| `int \| None` | 9 | 6 |
| `float \| None` | 9 | 5 |
| `bool \| None` | 1 | 1 |
| `dict \| None` | 2 | 2 |
| Union khác (`WorkflowEngine \| None`, `bytes \| None`, …) | ~40 | nhiều file |

### Top file theo union types

| File | Số dòng `X \| Y` |
|------|-------------------|
| `app/services/event_query_service.py` | 21 |
| `app/events/event_catalog.py` | 13 |
| `app/schemas/system.py` | 11 |
| `app/schemas/map.py` | 9 |
| `app/services/camera_snapshot_service.py` | 8 |
| `app/biosecurity_workflow/workflow_engine.py` | 5 |
| `app/schemas/smart_farm.py` | 5 |
| `app/api/deployment.py` | 4 |

### File API dùng `str \| None` trong Query params (blocker trên 3.9)

| File | Dòng |
|------|------|
| `app/api/cameras.py` | L40 |
| `app/api/deployment.py` | L84–87 |
| `app/api/farms.py` | L41 |
| `app/api/users.py` | L34 |
| `app/api/zones.py` | L99 |

---

## match / case

**Không sử dụng** structural pattern matching (`match`/`case` statement).

Các kết quả grep `match` trong repo là biến hoặc hàm (`match_uniform`, `match = ...`), không phải Python 3.10 `match/case`.

---

## Vì sao yêu cầu 3.11+ (không chỉ 3.10)

1. **PEP 604** (`X | Y`) — bắt buộc trên hàng chục file không có `from __future__ import annotations`.
2. **FastAPI / Pydantic v2** — phát triển và test trên 3.11+.
3. **Tiêu chuẩn dự án** — INSTALL, deployment docs, CI target **3.11+**.
4. **Support lifecycle** — Python 3.9/3.10 gần hoặc đã EOL; 3.11+ an toàn cho production.

---

## Phụ lục — Danh sách đầy đủ từng file / dòng

## A. Union types (`X | Y`)


### app/api/cameras.py (1 lines)
  L40: farm_id: str | None = Query(default=None),

### app/api/deployment.py (4 lines)
  L84: farmId: str | None = Query(default=None),
  L85: cameraId: str | None = Query(default=None),
  L86: date: str | None = Query(default=None, description="YYYY-MM-DD"),
  L87: ruleType: str | None = Query(default=None),

### app/api/farms.py (1 lines)
  L41: farm_id: str | None = Query(default=None),

### app/api/users.py (1 lines)
  L34: farm_id: str | None = Query(default=None),

### app/api/zones.py (1 lines)
  L99: camera_id: str | None = Query(default=None),

### app/biosecurity_workflow/definitions.py (2 lines)
  L19: def zone_for_step(self, step_code: str) -> str | None:
  L26: def step_for_zone(self, zone_code: str) -> str | None:

### app/biosecurity_workflow/workflow_engine.py (5 lines)
  L21: event_type: str | None = None
  L23: current_step: str | None = None
  L36: workflow_id: str | None = None
  L67: ) -> WorkflowEvaluationResult | None:
  L145: _engine: BiosecurityWorkflowEngine | None = None

### app/biosecurity_workflow/workflow_manager.py (2 lines)
  L17: def get_definition(self, workflow_id: str) -> WorkflowDefinition | None:
  L33: _manager: WorkflowManager | None = None

### app/biosecurity_workflow/workflow_state_store.py (1 lines)
  L58: _store: WorkflowStateStore | None = None

### app/compliance/compliance_engine.py (2 lines)
  L16: _engine: "ComplianceEngine | None" = None
  L22: def __init__(self, rules: Iterable[BaseComplianceRule] | None = None) -> None:

### app/compliance/evidence_snapshot.py (3 lines)
  L22: bbox: list[float] | tuple[float, float, float, float] | None = None,
  L24: ) -> str | None:
  L56: bbox: list[float] | tuple[float, float, float, float] | None,

### app/compliance/uniform_matcher.py (3 lines)
  L14: person_image: bytes | None,
  L17: track_id: int | None = None,
  L18: template_id: str | None = None,

### app/core/detectors/capabilities.py (3 lines)
  L42: last_error: str | None = None
  L43: started_at: str | None = None
  L44: stopped_at: str | None = None

### app/core/detectors/detector_registry.py (1 lines)
  L38: _registry: DetectorRegistry | None = None

### app/core/detectors/yolo_class_mapper.py (2 lines)
  L21: def map_yolo_class(class_name: str) -> str | None:
  L28: def map_coco_class_id(class_id: int, names: dict[int, str] | list[str]) -> str | None:

### app/core/detectors/yolo_detector_adapter.py (1 lines)
  L31: def parse_video_source(source: str) -> str | int:

### app/core/detectors/yolo_observation_mapper.py (2 lines)
  L36: attributes: dict[str, Any] | None = None,
  L54: timestamp: str | None = None,

### app/core/event_bus/event_bus.py (1 lines)
  L51: _event_bus: InMemoryEventBus | None = None

### app/core/farm_access.py (3 lines)
  L19: def assert_farm_access(user: User, farm_id: str | None) -> None:
  L30: def resolve_farm_scope(user: User, requested_farm_id: str | None = None) -> str | None:
  L36: def assert_can_manage_farm(user: User, farm_id: str | None) -> None:

### app/core/roles.py (1 lines)
  L52: def normalize_role(role: str | None) -> str:

### app/core/runtime/track_store.py (1 lines)
  L66: _track_store: TrackStore | None = None

### app/core/runtime/zone_presence_tracker.py (3 lines)
  L59: timestamp: str | None = None,
  L117: monitored_zone_ids: set[str] | None = None,
  L145: _tracker: ZonePresenceTracker | None = None

### app/events/event_catalog.py (13 lines)
  L120: def normalize_event_type(event_type: str | None) -> str | None:
  L128: event_type: str | None,
  L130: category: str | None = None,
  L141: event_type: str | None,
  L143: fallback: str | None = None,
  L166: event_type: str | None,
  L168: rule_name: str | None = None,
  L169: zone_name: str | None = None,
  L191: event_type: str | None,
  L192: category: str | None = None,
  L193: severity: str | None = None,
  L194: rule_name: str | None = None,
  L195: zone_name: str | None = None,

### app/schemas/map.py (9 lines)
  L32: layout_id: str | None = None
  L44: linked_camera_id: str | None = None
  L45: linked_zone_id: str | None = None
  L46: camera_direction: float | None = None
  L47: camera_fov: float | None = None
  L66: linked_camera_id: str | None = None
  L67: linked_zone_id: str | None = None
  L68: camera_direction: float | None = None
  L69: camera_fov: float | None = None

### app/schemas/smart_farm.py (5 lines)
  L35: linked_camera_id: str | None = None
  L36: linked_zone_id: str | None = None
  L37: camera_direction: float | None = None
  L38: camera_fov: float | None = None
  L76: layout_id: str | None = None

### app/schemas/system.py (11 lines)
  L14: compliance_threshold: float | None = Field(default=None, ge=0, le=1)
  L15: workflow_timeout: int | None = Field(default=None, ge=30, le=86400)
  L16: demo_mode: bool | None = None
  L17: retention_days: int | None = Field(default=None, ge=1, le=3650)
  L32: version: str | None = None
  L33: settings: dict[str, Any] | None = None
  L34: farms: list[dict[str, Any]] | None = None
  L35: cameras: list[dict[str, Any]] | None = None
  L36: zones: list[dict[str, Any]] | None = None
  L37: workflows: list[dict[str, Any]] | None = None
  L38: uniforms: list[dict[str, Any]] | None = None

### app/services/camera_connection_test.py (4 lines)
  L17: fps: int | None = None
  L18: resolution: str | None = None
  L19: error: str | None = None
  L22: def _parse_fps(value: str | None) -> int | None:

### app/services/camera_editor_zone_service.py (1 lines)
  L47: def get_editor_zone_or_none(db: Session, zone_id: str) -> CameraEditorZone | None:

### app/services/camera_registry.py (1 lines)
  L24: rtsp_url: str | None = None,

### app/services/camera_snapshot_service.py (8 lines)
  L18: url: str | None = None
  L19: error: str | None = None
  L20: captured_at: str | None = None
  L21: file_path: Path | None = None
  L35: def build_snapshot_filename(captured_at: datetime | None = None) -> str:
  L44: def resolve_camera_rtsp_url(camera: Camera) -> str | None:
  L58: def _validate_camera_for_capture(camera: Camera) -> CameraSnapshotResult | None:
  L76: captured_at: datetime | None = None,

### app/services/camera_zone_service.py (1 lines)
  L97: def get_camera_zone_or_none(db: Session, zone_id: str) -> CameraZone | None:

### app/services/compliance_report_service.py (3 lines)
  L52: days: int | None = None,
  L53: date_prefix: str | None = None,
  L84: def build_period_summary(db: Session, *, days: int | None = None, date_prefix: str | None = None) -> dict:

### app/services/demo_data_generator.py (1 lines)
  L57: farm_id: str | None = None,

### app/services/demo_event_generator.py (2 lines)
  L58: self._task: asyncio.Task | None = None
  L77: def _pick_demo_camera(self, db: Session, event_type: str) -> tuple[Camera, CameraZone | None]:

### app/services/demo_mode_service.py (1 lines)
  L9: def is_demo_mode(db: Session | None = None) -> bool:

### app/services/deployment_setup_service.py (4 lines)
  L88: track_id: int | None = None,
  L89: camera_id: str | None = None,
  L90: zone_id: str | None = None,
  L91: score_input: float | None = None,

### app/services/evaluator_event_service.py (4 lines)
  L98: track_id: int | None,
  L100: snapshot_path: str | None,
  L101: timestamp: str | None = None,
  L102: evidence: dict | None = None,

### app/services/event_query_service.py (21 lines)
  L12: event_type: str | None = None,
  L13: camera_id: str | None = None,
  L14: zone_id: str | None = None,
  L15: event_types: set[str] | None = None,
  L16: date_prefix: str | None = None,
  L17: since_iso: str | None = None,
  L18: categories: set[str] | None = None,
  L42: event_type: str | None = None,
  L43: camera_id: str | None = None,
  L44: zone_id: str | None = None,
  L45: event_types: set[str] | None = None,
  L46: date_prefix: str | None = None,
  L47: since_iso: str | None = None,
  L48: categories: set[str] | None = None,
  L75: event_type: str | None = None,
  L76: camera_id: str | None = None,
  L77: zone_id: str | None = None,
  L78: event_types: set[str] | None = None,
  L79: date_prefix: str | None = None,
  L80: since_iso: str | None = None,
  L81: categories: set[str] | None = None,

### app/services/event_stream_service.py (1 lines)
  L30: self._loop: asyncio.AbstractEventLoop | None = None

### app/services/evidence_browser_service.py (4 lines)
  L14: farm_id: str | None = None,
  L15: camera_id: str | None = None,
  L16: date_prefix: str | None = None,
  L17: rule_type: str | None = None,

### app/services/mock_rule_engine.py (1 lines)
  L22: def trigger_rule(db: Session, rule_id: str, *, confidence: float | None = None) -> Event:

### app/services/observation_service.py (1 lines)
  L85: def get_observation_or_none(db: Session, observation_id: str) -> Observation | None:

### app/services/snapshot_generator.py (1 lines)
  L238: def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:

### app/services/system_settings_service.py (1 lines)
  L50: updated_by: str | None = None,

### app/services/zone_rule_service.py (1 lines)
  L56: def get_zone_rule_or_none(db: Session, rule_id: str) -> ZoneRule | None:

### app/workers/detector_worker.py (2 lines)
  L50: payload: dict[str, Any] | None = None,
  L51: headers: dict[str, str] | None = None,

### scripts/simulate_workflow_v31.py (1 lines)
  L14: def cross(track_id: int, zone_id: str, timestamp: str) -> dict | None:


## B. Builtin generics (`list[str]`, `dict[str, Any]`, …)


### app/api/ai_detections.py (2 lines)
  L31: @router.get("/cameras/{camera_id}/detections", response_model=list[AiDetectionResponse])
  L32: def list_camera_detections(camera_id: str, db: Session = Depends(get_db)) -> list[AiDetectionResponse]:

### app/api/ai_models.py (2 lines)
  L15: @router.get("", response_model=list[AIModelResponse])
  L16: def list_ai_models(db: Session = Depends(get_db)) -> list[AIModel]:

### app/api/animal_intrusion.py (5 lines)
  L29: @router.get("/policies", response_model=list[AnimalIntrusionPolicyResponse])
  L30: def list_policies(db: Session = Depends(get_db)) -> list[AnimalIntrusionPolicy]:
  L95: @router.post("/policies/seed-defaults", response_model=list[AnimalIntrusionPolicyResponse])
  L96: def seed_default_policies(db: Session = Depends(get_db)) -> list[AnimalIntrusionPolicy]:
  L97: seeded: list[AnimalIntrusionPolicy] = []

### app/api/audit.py (2 lines)
  L17: @router.get("", response_model=list[AuditLogResponse])
  L24: ) -> list[AuditLog]:

### app/api/biosecurity_rules.py (8 lines)
  L69: @router.get("/farm-areas", response_model=list[FarmAreaTypeResponse])
  L70: def list_farm_area_types() -> list[FarmAreaTypeResponse]:
  L82: @router.get("/categories", response_model=list[BiosecurityCategoryResponse])
  L83: def list_categories() -> list[BiosecurityCategoryResponse]:
  L87: @router.get("/enabled", response_model=list[BiosecurityRuleResponse])
  L88: def list_enabled_rules(db: Session = Depends(get_db)) -> list[BiosecurityRuleResponse]:
  L99: @router.get("", response_model=list[BiosecurityRuleResponse])
  L100: def list_rules(db: Session = Depends(get_db)) -> list[BiosecurityRuleResponse]:

### app/api/camera_health.py (2 lines)
  L26: @router.get("", response_model=list[CameraHealthResponse])
  L27: def list_camera_health(db: Session = Depends(get_db)) -> list[CameraHealth]:

### app/api/camera_zone_rules.py (2 lines)
  L27: @router.get("/cameras/{camera_id}/rules", response_model=list[ZoneRuleResponse])
  L28: def list_camera_rules(camera_id: str, db: Session = Depends(get_db)) -> list[ZoneRuleResponse]:

### app/api/camera_zones.py (2 lines)
  L33: @router.get("/cameras/{camera_id}/zones", response_model=list[CameraZoneResponse])
  L34: def list_camera_zones(camera_id: str, db: Session = Depends(get_db)) -> list[CameraZoneResponse]:

### app/api/cameras.py (2 lines)
  L38: @router.get("", response_model=list[CameraResponse])
  L43: ) -> list[CameraResponse]:

### app/api/compliance.py (5 lines)
  L37: def _violation_events(db: Session) -> list[Event]:
  L49: def _score(events: list[Event]) -> int:
  L58: def _trend(events: list[Event], days: int) -> list[dict]:
  L102: def compliance_top_zones(db: Session = Depends(get_db)) -> list[dict]:
  L121: def compliance_top_violations(db: Session = Depends(get_db)) -> list[dict]:

### app/api/dashboard.py (6 lines)
  L49: @router.get("/trends", response_model=list[DashboardTrendItem])
  L50: def dashboard_trends(db: Session = Depends(get_db)) -> list[DashboardTrendItem]:
  L59: @router.get("/top-cameras", response_model=list[DashboardTopCameraItem])
  L60: def dashboard_top_cameras(db: Session = Depends(get_db)) -> list[DashboardTopCameraItem]:
  L79: @router.get("/top-zones", response_model=list[DashboardTopZoneItem])
  L80: def dashboard_top_zones(db: Session = Depends(get_db)) -> list[DashboardTopZoneItem]:

### app/api/detectors.py (1 lines)
  L10: def list_detectors() -> list[dict]:

### app/api/devices.py (2 lines)
  L15: @router.get("", response_model=list[EdgeDeviceResponse])
  L16: def list_devices(db: Session = Depends(get_db)) -> list[EdgeDevice]:

### app/api/employees.py (2 lines)
  L44: @router.get("", response_model=list[EmployeeResponse])
  L50: ) -> list[Employee]:

### app/api/events.py (4 lines)
  L69: @router.get("/engine", response_model=list[EventEngineResponse])
  L70: def list_engine_events(db: Session = Depends(get_db)) -> list[EventEngineResponse]:
  L75: @router.get("/cameras/{camera_id}/timeline", response_model=list[EventEngineResponse])
  L76: def list_camera_timeline(camera_id: str, db: Session = Depends(get_db)) -> list[EventEngineResponse]:

### app/api/farm_zones.py (2 lines)
  L17: @router.get("", response_model=list[FarmZoneResponse])
  L21: ) -> list[FarmZone]:

### app/api/farms.py (2 lines)
  L39: @router.get("", response_model=list[FarmResponse])
  L44: ) -> list[FarmResponse]:

### app/api/gateways.py (2 lines)
  L15: @router.get("", response_model=list[NotificationGatewayResponse])
  L16: def list_notification_gateways(db: Session = Depends(get_db)) -> list[NotificationGateway]:

### app/api/licenses.py (2 lines)
  L15: @router.get("", response_model=list[LicenseResponse])
  L16: def list_licenses(db: Session = Depends(get_db)) -> list[License]:

### app/api/map.py (4 lines)
  L46: @router.get("", response_model=list[FarmMapObjectResponse])
  L47: def list_map_objects(db: Session = Depends(get_db)) -> list[FarmMapObject]:
  L130: @router.get("/layouts", response_model=list[FarmMapLayoutResponse])
  L131: def list_layouts(db: Session = Depends(get_db)) -> list[FarmMapLayout]:

### app/api/notifications.py (2 lines)
  L15: @router.get("", response_model=list[NotificationRuleResponse])
  L16: def list_notification_rules(db: Session = Depends(get_db)) -> list[NotificationRule]:

### app/api/observations.py (4 lines)
  L33: camera_ids: list[str] = Field(min_length=1)
  L68: @router.get("/cameras/{camera_id}/observations", response_model=list[ObservationResponse])
  L73: ) -> list[ObservationResponse]:
  L98: def list_observation_fixtures() -> list[str]:

### app/api/realtime.py (1 lines)
  L10: self.active_connections: list[WebSocket] = []

### app/api/rules.py (2 lines)
  L72: @router.get("", response_model=list[BiosecurityRuleResponse])
  L73: def list_biosecurity_rules(db: Session = Depends(get_db)) -> list[BiosecurityRuleResponse]:

### app/api/snapshots.py (2 lines)
  L15: @router.get("", response_model=list[EventSnapshotResponse])
  L16: def list_snapshots(db: Session = Depends(get_db)) -> list[EventSnapshot]:

### app/api/streams.py (2 lines)
  L15: @router.get("", response_model=list[CameraStreamResponse])
  L16: def list_streams(db: Session = Depends(get_db)) -> list[CameraStream]:

### app/api/tasks.py (2 lines)
  L21: @router.get("", response_model=list[AITaskResponse])
  L22: def list_tasks(db: Session = Depends(get_db)) -> list[AITask]:

### app/api/templates.py (6 lines)
  L20: @router.get("", response_model=list[FarmLayoutTemplateSummaryResponse])
  L21: def list_templates(db: Session = Depends(get_db)) -> list[FarmLayoutTemplateSummaryResponse]:
  L41: @router.get("/zone-codes", response_model=list[str])
  L42: def list_zone_codes() -> list[str]:
  L68: @router.get("/{template_id}/zones", response_model=list[TemplateZoneDefinitionResponse])
  L69: def list_template_zones(template_id: str, db: Session = Depends(get_db)) -> list[TemplateZoneDefinition]:

### app/api/tracks.py (4 lines)
  L24: @router.get("", response_model=list[ObjectTrackResponse])
  L30: ) -> list[dict]:
  L52: @router.post("/sync", response_model=list[ObjectTrackResponse])
  L53: def sync_camera_tracks(payload: ObjectTrackSyncRequest, db: Session = Depends(get_db)) -> list[dict]:

### app/api/transitions.py (2 lines)
  L28: @router.get("", response_model=list[ZoneTransitionResponse])
  L29: def list_transitions(db: Session = Depends(get_db)) -> list[ZoneTransition]:

### app/api/uniforms.py (2 lines)
  L27: @router.get("", response_model=list[UniformTemplateResponse])
  L31: ) -> list[UniformTemplateResponse]:

### app/api/users.py (2 lines)
  L32: @router.get("", response_model=list[UserResponse])
  L37: ) -> list[UserResponse]:

### app/api/visitors.py (2 lines)
  L58: @router.get("", response_model=list[VisitorResponse])
  L63: ) -> list[VisitorResponse]:

### app/api/workflows.py (7 lines)
  L94: @router.get("/violation-types", response_model=list[WorkflowViolationType])
  L95: def list_workflow_violation_types() -> list[WorkflowViolationType]:
  L116: @router.get("/history", response_model=list[WorkflowHistoryItem])
  L122: ) -> list[WorkflowHistoryItem]:
  L126: @router.get("", response_model=list[WorkflowResponse])
  L130: ) -> list[WorkflowResponse]:
  L140: def list_biosecurity_workflow_definitions() -> list[dict]:

### app/api/zones.py (8 lines)
  L63: @router.get("/types", response_model=list[ZoneTypeOptionResponse])
  L64: def list_zone_types() -> list[ZoneTypeOptionResponse]:
  L77: @router.get("/classifications", response_model=list[ZoneClassificationResponse])
  L78: def list_zone_classifications() -> list[ZoneClassificationResponse]:
  L85: @router.get("/template", response_model=list[ZoneTemplateItemResponse])
  L86: def list_zone_template() -> list[ZoneTemplateItemResponse]:
  L97: @router.get("", response_model=list[ZonePolygonResponse])
  L101: ) -> list[ZonePolygonResponse]:

### app/biosecurity_workflow/constants.py (1 lines)
  L14: STEP_ZONE_CODES: dict[str, str] = {

### app/biosecurity_workflow/definitions.py (3 lines)
  L16: steps: list[str]
  L17: step_zones: dict[str, str] = field(default_factory=dict)
  L47: DEFAULT_WORKFLOW_DEFINITIONS: tuple[WorkflowDefinition, ...] = (ENTRY_CLEAN_ZONE_WORKFLOW,)

### app/biosecurity_workflow/integration.py (1 lines)
  L25: ) -> Optional[dict[str, Any]]:

### app/biosecurity_workflow/workflow_engine.py (5 lines)
  L24: skipped_steps: list[str] = field(default_factory=list)
  L25: completed_steps: list[str] = field(default_factory=list)
  L26: evidence: dict[str, Any] = field(default_factory=dict)
  L44: def evaluate(self, context: WorkflowEvaluationContext) -> list[WorkflowEvaluationResult]:
  L48: results: list[WorkflowEvaluationResult] = []

### app/biosecurity_workflow/workflow_manager.py (2 lines)
  L12: self._definitions: dict[str, WorkflowDefinition] = {}
  L20: def list_definitions(self) -> list[WorkflowDefinition]:

### app/biosecurity_workflow/workflow_state_store.py (2 lines)
  L10: completed_steps: list[str] = field(default_factory=list)
  L19: self._states: dict[str, TrackWorkflowState] = {}

### app/compliance/compliance_engine.py (5 lines)
  L23: self._rules: list[BaseComplianceRule] = list(rules or load_compliance_rules())
  L26: def rules(self) -> list[BaseComplianceRule]:
  L32: def list_managed_rules(self) -> list[dict[str, str]]:
  L38: def evaluate(self, context: ComplianceContext, *, publish: bool = True) -> list[ComplianceViolationEvent]:
  L39: violations: list[ComplianceViolationEvent] = []

### app/compliance/compliance_integration.py (4 lines)
  L15: hit: dict[str, Any],
  L16: track: dict[str, Any],
  L17: observation: dict[str, Any],
  L18: obj: dict[str, Any],

### app/compliance/compliance_rules.py (2 lines)
  L8: def build_default_compliance_rules() -> list[BaseComplianceRule]:
  L12: def list_managed_rule_definitions() -> list[ComplianceRuleDefinition]:

### app/compliance/constants.py (1 lines)
  L24: COMPLIANCE_RULE_DEFINITIONS: tuple[ComplianceRuleDefinition, ...] = (

### app/compliance/evidence_snapshot.py (2 lines)
  L22: bbox: list[float] | tuple[float, float, float, float] | None = None,
  L56: bbox: list[float] | tuple[float, float, float, float] | None,

### app/compliance/rule_registry.py (2 lines)
  L12: RULE_CLASSES: list[type[BaseComplianceRule]] = [
  L23: def load_compliance_rules() -> list[BaseComplianceRule]:

### app/compliance/types.py (5 lines)
  L15: evidence: dict[str, Any] = field(default_factory=dict)
  L29: evidence: dict[str, Any] = field(default_factory=dict)
  L31: def to_dict(self) -> dict[str, Any]:
  L54: observation: Optional[dict[str, Any]] = None
  L55: metadata: dict[str, Any] = field(default_factory=dict)

### app/compliance/uniform_matcher.py (1 lines)
  L15: template_images: list[str],

### app/core/config.py (1 lines)
  L43: def cors_origin_list(self) -> list[str]:

### app/core/detectors/capabilities.py (2 lines)
  L14: def to_dict(self) -> dict[str, bool]:
  L47: def to_dict(self) -> dict[str, Any]:

### app/core/detectors/detector_adapter.py (4 lines)
  L13: ObservationCallback = Callable[[dict[str, Any]], None]
  L50: def detect(self, context: dict[str, Any]) -> dict[str, Any]:
  L54: def to_dict(self) -> dict[str, Any]:
  L88: def _emit_observation(self, payload: dict[str, Any]) -> None:

### app/core/detectors/detector_registry.py (3 lines)
  L13: self._detectors: dict[str, DetectorAdapter] = {}
  L31: def list(self) -> list[DetectorAdapter]:
  L34: def list_dicts(self) -> list[dict]:

### app/core/detectors/mock_detector_adapter.py (2 lines)
  L19: SCENARIOS: dict[str, dict[str, Any]] = {
  L97: def detect(self, context: dict[str, Any]) -> dict[str, Any]:

### app/core/detectors/yolo_class_mapper.py (3 lines)
  L11: SUPPORTED_COCO_CLASS_IDS: tuple[int, ...] = (COCO_PERSON, COCO_BIRD, COCO_DOG, COCO_CAT)
  L13: YOLO_TO_AMS_CLASS: dict[str, str] = {
  L28: def map_coco_class_id(class_id: int, names: dict[int, str] | list[str]) -> str | None:

### app/core/detectors/yolo_detector_adapter.py (1 lines)
  L183: detections: list[DetectionInput] = []

### app/core/detectors/yolo_observation_mapper.py (6 lines)
  L16: ) -> dict[str, float]:
  L35: bbox: dict[str, float],
  L36: attributes: dict[str, Any] | None = None,
  L37: ) -> dict[str, Any]:
  L50: objects: list[dict[str, Any]],
  L56: ) -> dict[str, Any]:

### app/core/detectors/yolo_tracker.py (6 lines)
  L61: self._tracks: dict[str, TrackedBox] = {}
  L70: def update(self, detections: list[DetectionInput]) -> list[TrackedDetection]:
  L71: assigned: set[str] = set()
  L72: outputs: list[TrackedDetection] = []
  L151: def update(self, detections: list[DetectionInput]) -> list[TrackedDetection]:
  L177: outputs: list[TrackedDetection] = []

### app/core/event_bus/event_bus.py (4 lines)
  L10: EventHandler = Callable[[dict[str, Any]], None]
  L15: def publish(self, topic: str, payload: dict[str, Any]) -> None:
  L29: self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)
  L31: def publish(self, topic: str, payload: dict[str, Any]) -> None:

### app/core/observation_schema.py (1 lines)
  L20: def migrate_observation_payload(payload: dict[str, Any]) -> dict[str, Any]:

### app/core/roles.py (1 lines)
  L19: PERMISSIONS: dict[str, set[str]] = {

### app/core/runtime/track_store.py (5 lines)
  L12: self._tracks: dict[str, dict[str, Any]] = {}
  L23: metadata: Optional[dict[str, Any]] = None,
  L24: ) -> tuple[dict[str, Any], bool, Optional[dict[str, Any]]]:
  L52: def get_track(self, camera_id: str, track_id: str) -> Optional[dict[str, Any]]:
  L58: def get_tracks_by_camera(self, camera_id: str) -> list[dict[str, Any]]:

### app/core/runtime/zone_mapper.py (5 lines)
  L8: def map_observation_to_zones(observation: dict[str, Any], zones: list[dict[str, Any]]) -> list[dict[str, Any]]:
  L9: mappings: list[dict[str, Any]] = []
  L16: zones_matched: list[str] = []
  L17: subzones_matched: list[str] = []
  L47: def object_in_zone(mapping: dict[str, Any], zone_id: str) -> bool:

### app/core/runtime/zone_presence_tracker.py (5 lines)
  L30: self._states: dict[str, str] = {}
  L31: self._records: dict[str, dict] = {}
  L115: active_zone_ids: set[str],
  L117: monitored_zone_ids: set[str] | None = None,
  L118: ) -> dict[str, ZoneTransitionResult]:

### app/core/security.py (2 lines)
  L52: def create_access_token(subject: str, role: str) -> tuple[str, int, str]:
  L85: def decode_access_token(token: str) -> Optional[dict[str, Any]]:

### app/data/workflow_defaults.py (1 lines)
  L59: def build_workflow_steps(workflow_id: str, final_step: tuple[str, str]) -> list[tuple[str, int, str, str]]:

### app/events/event_catalog.py (4 lines)
  L20: def to_dict(self) -> dict[str, str]:
  L35: EVENT_CATALOG: dict[str, EventCatalogEntry] = {
  L170: ) -> dict[str, str]:
  L196: ) -> dict[str, Any]:

### app/models/camera_editor_zone.py (1 lines)
  L17: points: Mapped[list[dict]] = mapped_column(JSON, nullable=False)

### app/models/camera_zone.py (1 lines)
  L27: points: Mapped[list[dict]] = mapped_column(JSON, nullable=False)

### app/models/observation.py (1 lines)
  L23: objects: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False)

### app/models/uniform_template.py (1 lines)
  L19: image_paths: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

### app/models/zone_polygon.py (1 lines)
  L19: polygon_points: Mapped[list[list[float]]] = mapped_column(JSON, nullable=False)

### app/models/zone_rule.py (1 lines)
  L39: config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

### app/schemas/animal_intrusion.py (4 lines)
  L8: allowed_zones: list[str] = Field(default_factory=list)
  L9: restricted_zones: list[str] = Field(default_factory=list)
  L19: allowed_zones: Optional[list[str]] = None
  L20: restricted_zones: Optional[list[str]] = None

### app/schemas/camera_editor_zone.py (3 lines)
  L23: points: list[ZonePoint] = Field(min_length=3)
  L55: points: Optional[list[ZonePoint]] = Field(default=None, min_length=3)
  L95: points: list[ZonePoint]

### app/schemas/camera_zone.py (3 lines)
  L35: points: list[ZonePoint] = Field(min_length=3)
  L79: points: Optional[list[ZonePoint]] = Field(default=None, min_length=3)
  L123: points: list[ZonePointNormalized]

### app/schemas/dashboard.py (1 lines)
  L17: top_quy_tac_atsh: list[dict] = []

### app/schemas/deployment.py (10 lines)
  L12: websocket: dict[str, Any]
  L13: storage: dict[str, Any]
  L14: camera: dict[str, Any]
  L15: ffmpeg: dict[str, Any]
  L27: farm: Optional[list[dict[str, Any]]] = Field(default=None, alias="farm.json")
  L28: camera: Optional[list[dict[str, Any]]] = Field(default=None, alias="camera.json")
  L29: zone: Optional[list[dict[str, Any]]] = Field(default=None, alias="zone.json")
  L30: workflow: Optional[list[dict[str, Any]]] = Field(default=None, alias="workflow.json")
  L31: settings: Optional[dict[str, Any]] = Field(default=None, alias="settings.json")
  L32: uniform: Optional[list[dict[str, Any]]] = Field(default=None, alias="uniform.json")

### app/schemas/event.py (3 lines)
  L44: metadata: Optional[dict[str, Any]] = Field(default=None, alias="event_metadata")
  L54: explanation: Optional[dict[str, Any]] = None
  L60: items: list[EventEngineResponse]

### app/schemas/farm_template.py (1 lines)
  L29: zones: list[TemplateZoneDefinitionResponse] = []

### app/schemas/map.py (2 lines)
  L75: objects: list[FarmMapObjectInput] = Field(default_factory=list)
  L80: objects: list[FarmMapObjectResponse]

### app/schemas/object_track.py (1 lines)
  L20: tracks: list[ObjectTrackSyncItem]

### app/schemas/observation.py (4 lines)
  L29: attributes: dict[str, Any] = Field(default_factory=dict)
  L50: objects: list[ObservationObject] = Field(default_factory=list)
  L77: objects: list[dict[str, Any]]
  L92: event_metadata: Optional[dict[str, Any]] = None

### app/schemas/person_track.py (1 lines)
  L17: lich_su_vung: list[PersonTrackVisitResponse] = []

### app/schemas/smart_farm.py (12 lines)
  L18: points: list[list[float]] = Field(default_factory=list)
  L19: labels: list[str] = Field(default_factory=list)
  L55: objects: list[FarmObjectInput] = Field(default_factory=list)
  L56: routes: list[FarmRouteInput] = Field(default_factory=list)
  L57: layers: list[FarmMapLayerInput] = Field(default_factory=list)
  L86: points: list[list[float]]
  L87: labels: list[str]
  L105: objects: list[FarmObjectResponse]
  L106: routes: list[FarmRouteResponse]
  L107: layers: list[FarmMapLayerResponse]
  L110: def parse_route_points(raw: str) -> list[list[float]]:
  L117: def parse_route_labels(raw: str) -> list[str]:

### app/schemas/system.py (12 lines)
  L23: settings: dict[str, Any]
  L24: farms: list[dict[str, Any]]
  L25: cameras: list[dict[str, Any]]
  L26: zones: list[dict[str, Any]]
  L27: workflows: list[dict[str, Any]]
  L28: uniforms: list[dict[str, Any]]
  L33: settings: dict[str, Any] | None = None
  L34: farms: list[dict[str, Any]] | None = None
  L35: cameras: list[dict[str, Any]] | None = None
  L36: zones: list[dict[str, Any]] | None = None
  L37: workflows: list[dict[str, Any]] | None = None
  L38: uniforms: list[dict[str, Any]] | None = None

### app/schemas/transition.py (1 lines)
  L38: items: list[ZoneTransitionResponse]

### app/schemas/uniform.py (3 lines)
  L11: image_paths: list[str]
  L21: image_paths: list[str] = Field(default_factory=list)
  L28: image_paths: Optional[list[str]] = None

### app/schemas/workflow.py (9 lines)
  L33: steps: list[WorkflowStepBase] = Field(min_length=1)
  L41: steps: Optional[list[WorkflowStepBase]] = None
  L50: steps: list[WorkflowStepResponse] = []
  L64: top_quy_trinh_bi_vi_pham: list[dict]
  L65: expected_steps: list[str]
  L66: recent_violations: list[dict]
  L79: cac_vung_da_di: list[dict] = []
  L85: top_quy_trinh_bi_vi_pham: list[dict]
  L86: chi_tiet_hom_nay: list[dict]

### app/schemas/zone.py (3 lines)
  L26: polygon_points: list[list[float]] = Field(min_length=3)
  L43: polygon_points: Optional[list[list[float]]] = Field(default=None, min_length=3)
  L59: diem_polygon: list[list[float]]

### app/schemas/zone_rule.py (3 lines)
  L16: config: dict[str, Any] = Field(default_factory=dict)
  L53: config: Optional[dict[str, Any]] = None
  L98: config: dict[str, Any]

### app/services/ai_detection_service.py (1 lines)
  L41: def list_detections_for_camera(db: Session, camera_id: str) -> list[AiDetection]:

### app/services/atsh_biosecurity_engine.py (3 lines)
  L186: by_rule: dict[str, int] = {}
  L339: truck_zones: set[str],
  L340: truck_types: set[str],

### app/services/atsh_pipeline.py (10 lines)
  L20: zone_history: list[dict] = field(default_factory=list)
  L21: workflow_progress: list[dict] = field(default_factory=list)
  L22: active_workflows: list[dict] = field(default_factory=list)
  L30: self._post_workflow_hooks: list[str] = [
  L37: def registered_engines(self) -> list[str]:
  L40: def run_post_workflow(self, db: Session, context: WorkflowContext) -> list[dict]:
  L42: results: list[dict] = []
  L63: zone_history: list[dict],
  L64: progress_rows: list[TrackWorkflowProgress],
  L65: workflows: list[Workflow],

### app/services/backup_service.py (2 lines)
  L22: def export_backup(db: Session) -> dict[str, Any]:
  L119: def restore_backup(db: Session, payload: dict[str, Any]) -> dict[str, int]:

### app/services/camera_editor_zone_service.py (2 lines)
  L33: def _points_payload(points: list) -> list[dict]:
  L37: def list_zones_for_camera(db: Session, camera_id: str) -> list[CameraEditorZone]:

### app/services/camera_health_service.py (2 lines)
  L113: def evaluate_statuses(self, db: Session, *, now: Optional[datetime] = None) -> list[CameraHealth]:
  L115: updated: list[CameraHealth] = []

### app/services/camera_zone_service.py (4 lines)
  L53: def _points_payload(points: list) -> list[dict]:
  L58: points: list[dict],
  L61: ) -> tuple[list[dict], str, Optional[int], Optional[int]]:
  L87: def list_zones_for_camera(db: Session, camera_id: str) -> list[CameraZone]:

### app/services/compliance_report_service.py (5 lines)
  L54: ) -> list[Event]:
  L64: def _compliance_score(events: list[Event]) -> int:
  L73: def _count_by_classification(events: list[Event]) -> dict[str, int]:
  L129: def build_top_violations(db: Session, *, days: int = 7, limit: int = 10) -> list[dict]:
  L131: grouped: dict[str, dict] = defaultdict(lambda: {"count": 0, "severity": "MEDIUM", "classification": "BIOSECURITY"})

### app/services/demo_assets_service.py (1 lines)
  L10: ASSET_SPECS: tuple[tuple[str, str, str], ...] = (

### app/services/demo_bootstrap_service.py (1 lines)
  L16: DEMO_CAMERAS: tuple[tuple[str, str, str, str], ...] = (

### app/services/demo_data_generator.py (2 lines)
  L58: ) -> list[Event]:
  L66: created: list[Event] = []

### app/services/demo_event_generator.py (1 lines)
  L77: def _pick_demo_camera(self, db: Session, event_type: str) -> tuple[Camera, CameraZone | None]:

### app/services/deployment_config_service.py (2 lines)
  L10: def export_config_files(db: Session) -> dict[str, Any]:
  L27: def import_config_files(db: Session, payload: dict[str, Any]) -> dict[str, int]:

### app/services/deployment_diagnostics_service.py (7 lines)
  L17: def _disk_diagnostics() -> dict[str, Any]:
  L27: def _memory_diagnostics() -> dict[str, Any]:
  L45: def _cpu_diagnostics() -> dict[str, Any]:
  L58: def _gpu_diagnostics() -> dict[str, Any]:
  L78: def _network_diagnostics() -> dict[str, Any]:
  L87: def _camera_reachability(db: Session, limit: int = 10) -> list[dict[str, Any]]:
  L118: def build_diagnostics_report(db: Session) -> dict[str, Any]:

### app/services/deployment_health_service.py (5 lines)
  L18: def _check_storage() -> dict[str, Any]:
  L39: def _check_ffmpeg() -> dict[str, Any]:
  L52: def _check_cameras(db: Session) -> dict[str, Any]:
  L78: def _check_websocket() -> dict[str, Any]:
  L87: def build_health_report(db: Session) -> dict[str, Any]:

### app/services/deployment_setup_service.py (3 lines)
  L17: def get_setup_status(db: Session) -> dict[str, Any]:
  L43: def test_zone(db: Session, zone_id: str) -> dict[str, Any]:
  L92: ) -> dict[str, Any]:

### app/services/employee_tracking.py (2 lines)
  L21: def sync_tracks(db: Session, items: list[ObjectTrackSyncItem]) -> list[ObjectTrack]:
  L22: synced: list[ObjectTrack] = []

### app/services/event_engine_service.py (1 lines)
  L76: def list_events_for_camera(db: Session, camera_id: str) -> list[Event]:

### app/services/event_query_service.py (8 lines)
  L15: event_types: set[str] | None = None,
  L18: categories: set[str] | None = None,
  L45: event_types: set[str] | None = None,
  L48: categories: set[str] | None = None,
  L49: ) -> tuple[list[Event], int]:
  L78: event_types: set[str] | None = None,
  L81: categories: set[str] | None = None,
  L82: ) -> list[Event]:

### app/services/event_stream_service.py (2 lines)
  L45: async def _broadcast_all(self, message: dict[str, Any]) -> None:
  L54: def _forward_to_websocket(self, payload: dict[str, Any]) -> None:

### app/services/evidence_browser_service.py (1 lines)
  L20: ) -> tuple[list[dict], int]:

### app/services/observation_replay_service.py (5 lines)
  L22: def load_fixture(self, fixture_name: str) -> dict[str, Any]:
  L29: def list_fixtures(self) -> list[str]:
  L41: ) -> dict[str, Any]:
  L73: camera_ids: list[str],
  L75: ) -> list[dict[str, Any]]:

### app/services/observation_service.py (2 lines)
  L25: def _serialize_objects(objects: list) -> list[dict[str, Any]]:
  L94: ) -> list[Observation]:

### app/services/observation_validator.py (3 lines)
  L15: def validate(self, payload: dict[str, Any]) -> ObservationCreate:
  L39: def _validate_object(self, obj: dict[str, Any], index: int) -> None:
  L63: def _normalize_object(self, obj: dict[str, Any]) -> dict[str, Any]:

### app/services/pipeline_subscribers.py (20 lines)
  L30: def _publish(topic: str, data: dict[str, Any]) -> None:
  L41: def handle_observation_created(message: dict[str, Any]) -> None:
  L103: def handle_track_updated(message: dict[str, Any]) -> None:
  L145: def handle_event_created(message: dict[str, Any]) -> None:
  L166: def _active_zone_ids(zone_mapping: Optional[dict[str, Any]]) -> set[str]:
  L176: track: dict[str, Any],
  L178: observation: dict[str, Any],
  L198: track: dict[str, Any],
  L199: zone_mapping: Optional[dict[str, Any]],
  L201: observation: dict[str, Any],
  L202: ) -> dict[str, Any]:
  L222: track: dict[str, Any],
  L223: observation: dict[str, Any],
  L224: zone_mapping: Optional[dict[str, Any]],
  L227: ) -> list[dict[str, Any]]:
  L231: hits: list[dict[str, Any]] = []
  L313: observation: dict[str, Any],
  L314: zones: list[dict[str, Any]],
  L315: mappings: list[dict[str, Any]],
  L369: def _build_hit(rule, track, observation, obj, confidence: float, extra: Optional[dict] = None) -> dict[str, Any]:

### app/services/retention_service.py (1 lines)
  L21: def run_retention_cleanup(db: Session) -> dict[str, int]:

### app/services/runtime_metrics_service.py (6 lines)
  L31: _observation_window: list[float] = field(default_factory=list)
  L32: _event_window: list[float] = field(default_factory=list)
  L53: def refresh_runtime(self, db: Session, detector_count: int) -> dict[str, Any]:
  L63: def to_dict(self) -> dict[str, Any]:
  L82: def on_observation(_message: dict[str, Any]) -> None:
  L85: def on_event(_message: dict[str, Any]) -> None:

### app/services/snapshot_generator.py (3 lines)
  L35: bbox: Optional[tuple[int, int, int, int]] = None
  L68: ) -> tuple[str, str]:
  L218: def _default_bbox(track_id: Optional[int]) -> tuple[int, int, int, int]:

### app/services/system_settings_service.py (4 lines)
  L25: def _defaults() -> dict[str, Any]:
  L35: def get_system_settings(db: Session) -> dict[str, Any]:
  L48: payload: dict[str, Any],
  L51: ) -> dict[str, Any]:

### app/services/workflow_engine.py (9 lines)
  L108: ) -> list[dict]:
  L169: workflow_counts: dict[str, int] = {}
  L358: skipped_steps: list[WorkflowStep],
  L380: skipped_steps: list[str],
  L467: def _resolve_violation_codes(skipped_steps: list[WorkflowStep]) -> list[str]:
  L468: codes: list[str] = []
  L476: def _load_zone_history(db: Session, *, track_id: int) -> list[dict]:
  L501: def _load_steps(db: Session, workflow_id: str) -> list[WorkflowStep]:
  L511: def _match_step(steps: list[WorkflowStep], zone_code: str) -> Optional[WorkflowStep]:

### app/services/zone_rule_service.py (1 lines)
  L46: def list_rules_for_camera(db: Session, camera_id: str) -> list[ZoneRule]:

### app/utils/zone_geometry.py (6 lines)
  L32: points: list[dict],
  L35: ) -> list[dict]:
  L40: points: list[dict],
  L51: points: list[dict],
  L58: ) -> list[dict]:
  L77: def point_in_polygon(point: dict, polygon: list[dict]) -> bool:

### app/workers/detector_worker.py (6 lines)
  L50: payload: dict[str, Any] | None = None,
  L51: headers: dict[str, str] | None = None,
  L53: ) -> dict[str, Any]:
  L85: def _build_ingest_handler(config: DetectorWorkerConfig) -> Callable[[dict[str, Any]], None]:
  L89: def ingest_api(payload: dict[str, Any]) -> None:
  L103: def ingest_local(payload: dict[str, Any]) -> None:

### app/ws/connection_manager.py (1 lines)
  L22: async def broadcast(self, message: dict[str, Any]) -> None:

### tests/test_evaluator_harness.py (1 lines)
  L17: received: list[dict] = []

### tests/test_event_bus.py (3 lines)
  L10: received: list[dict] = []
  L23: received: list[dict] = []
  L36: received: list[dict] = []

### tests/test_zone_presence_tracker.py (1 lines)
  L54: def _collect(self, results) -> list[str]:

### scripts/simulate_workflow_v31.py (2 lines)
  L34: zones: list[str],
  L35: expected_codes: set[str],


---

## Tài liệu liên quan

- [INSTALL.md](./INSTALL.md)
- [README.md](./README.md)
- [docs/AMS_DEPLOYMENT_GUIDE.md](./docs/AMS_DEPLOYMENT_GUIDE.md)

*Generated by backend static scan — 2026-06-18.*
