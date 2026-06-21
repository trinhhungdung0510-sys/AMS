# AMS Implementation Audit

**Phạm vi:** v1.7 Compliance Framework · v1.8 Biosecurity Workflow · v1.8.1 Event Catalog · v1.9 RC1 · v2.0 Deployment/Demo  
**Ngày audit:** 2026-06-18  
**Loại:** Post-implementation validation — không thêm tính năng

---

## 1. File mới (chính)

### Backend — Compliance (v1.7)

| File | Mục đích |
|------|----------|
| `backend/app/compliance/compliance_engine.py` | ComplianceEngine |
| `backend/app/compliance/rule_registry.py` | RuleRegistry |
| `backend/app/compliance/compliance_integration.py` | Hook pipeline person-enter |
| `backend/app/compliance/compliance_event_service.py` | Event emission helpers |
| `backend/app/compliance/evidence_snapshot.py` | Evidence JPEG `uploads/evidence/YYYY/MM/DD/` |
| `backend/app/compliance/uniform_matcher.py` | Uniform matching |
| `backend/app/compliance/rules/base.py` | BaseComplianceRule |
| `backend/app/compliance/rules/uniform_rule.py` | UniformRule |
| `backend/app/compliance/rules/animal_intrusion_rule.py` | AnimalIntrusionRule |
| `backend/app/compliance/rules/zone_intrusion_rule.py` | ZoneIntrusionRule |
| `backend/app/compliance/rules/hand_sanitation_rule.py` | HandSanitationRule |
| `backend/app/compliance/rules/boot_sanitation_rule.py` | BootSanitationRule |
| `backend/app/compliance/rules/vehicle_sanitation_rule.py` | VehicleSanitationRule |
| `backend/app/compliance/rules/biosecurity_process_rule.py` | BiosecurityProcessRule |
| `backend/app/models/uniform_template.py` | UniformTemplate model |
| `backend/app/api/uniforms.py` | Uniform CRUD API |
| `backend/alembic/versions/0033_compliance_uniform_v17.py` | Migration uniform |

### Backend — Workflow (v1.8)

| File | Mục đích |
|------|----------|
| `backend/app/biosecurity_workflow/workflow_engine.py` | BiosecurityWorkflowEngine |
| `backend/app/biosecurity_workflow/workflow_manager.py` | init_workflow_manager |
| `backend/app/biosecurity_workflow/workflow_state_store.py` | In-memory workflow state |
| `backend/app/biosecurity_workflow/integration.py` | evaluate_biosecurity_process |
| `backend/app/biosecurity_workflow/definitions.py` | Step definitions |

### Backend — Event catalog & reports (v1.8.1)

| File | Mục đích |
|------|----------|
| `backend/app/events/event_catalog.py` | Classification, severity, explanation |
| `backend/app/services/compliance_report_service.py` | KPI, top violations, PDF data |
| `backend/app/api/reports.py` | `/api/reports/compliance/*` |

### Backend — RC1 / v2.0 (ops)

| File | Mục đích |
|------|----------|
| `backend/app/api/deployment.py` | Deployment kit API |
| `backend/app/api/demo.py` | Demo mode API |
| `backend/app/api/system.py` | System settings, backup |
| `backend/app/api/users.py` | User management |
| `backend/app/services/demo_event_generator.py` | DemoEventGenerator |
| `backend/app/services/demo_bootstrap_service.py` | Mind Farm Demo |
| `backend/demo-assets/*.jpg` | Demo snapshots |

### Frontend

| File | Mục đích |
|------|----------|
| `src/pages/ComplianceCenterPage.jsx` | Realtime compliance center |
| `src/components/compliance/*` | Event card, filters, evidence modal |
| `src/components/dashboard/ComplianceKpiWidgets.jsx` | Dashboard KPIs |
| `src/data/eventCatalog.js` | Event type catalog (mirror) |
| `src/data/complianceCenter.js` | Compliance filters/labels |
| `src/utils/complianceEventNormalizer.js` | Normalizer + snapshot URL |
| `src/pages/SetupWizardPage.jsx` | Setup wizard |
| `src/pages/DiagnosticsPage.jsx` | Diagnostics |
| `src/pages/SystemStatusPage.jsx` | System status |
| `src/pages/SnapshotBrowserPage.jsx` | Evidence browser |
| `src/services/deploymentService.js` | Deployment API client |
| `src/services/demoService.js` | Demo API client |
| `src/services/reportsService.js` | Reports API client |

### JS mirror (backend/src/modules/)

| File | Mirror |
|------|--------|
| `compliance/complianceEngine.js` | ComplianceEngine |
| `compliance/ruleRegistry.js` | RuleRegistry |
| `compliance/BaseRule.js` | BaseRule |
| `compliance/rules/*.js` | Individual rules |
| `workflow/workflowEngine.js` | Workflow engine |
| `events/eventCatalog.js` | Event catalog |

---

## 2. File đã sửa (chính)

### Backend

- `backend/app/main.py` — startup: compliance, workflow, pipeline, demo, deployment routers
- `backend/app/services/pipeline_subscribers.py` — compliance on person enter
- `backend/app/services/evaluator_event_service.py` — `create_compliance_violation_event`
- `backend/app/api/compliance.py` — expanded query endpoints
- `backend/app/api/workflows.py` — biosecurity definitions, compliance summary
- `backend/app/api/transitions.py` — workflow integration on zone cross
- `backend/app/api/events.py`, `farms.py`, `auth.py`, `cameras.py`, `camera_zones.py`
- `backend/app/core/config.py` — demo, retention, compliance settings

### Frontend

- `src/routes/AppRoutes.jsx` — routes mới
- `src/components/Sidebar.jsx` — navigation
- `src/pages/DashboardPage.jsx` — compliance KPI widgets
- `src/pages/SettingsPage.jsx` — system settings, demo controls
- `src/context/EventStore.jsx` — WS event handling
- `src/utils/eventNormalizer.js` — v1.8.1 fields
- `src/styles/ams-extensions.css` — compliance + deployment styles

---

## 3. API mới

Prefix: `/api` (trừ `/health`, `/ws/events`)

### Compliance (v1.7+)

| Method | Path |
|--------|------|
| GET | `/compliance/summary`, `/compliance/trends`, `/compliance/top-zones` |
| GET | `/compliance/top-violations`, `/compliance/events`, `/compliance/events/summary` |

### Uniforms (v1.7)

| Method | Path |
|--------|------|
| GET | `/uniforms` |
| POST | `/uniforms` |
| PUT | `/uniforms/{uniform_id}` |

### Reports (v1.8.1)

| Method | Path |
|--------|------|
| GET | `/reports/compliance` |
| GET | `/reports/compliance/kpis` |
| GET | `/reports/compliance/top-violations` |
| GET | `/reports/compliance/pdf-data` |

### Workflow (v1.8)

| Method | Path |
|--------|------|
| GET | `/workflows/definitions/biosecurity` |
| GET | `/workflows/compliance/summary` |
| GET | `/workflows/dashboard`, `/workflows/history`, `/workflows/pipeline` |

### Demo / Deployment (v2.0)

| Method | Path |
|--------|------|
| POST | `/demo/start`, `/demo/stop`, `/demo/generate-violations` |
| GET | `/demo/status` |
| GET | `/deployment/*`, `POST /deployment/import` |
| GET | `/health` (extended deployment health) |

### System / Users (v1.9)

| Method | Path |
|--------|------|
| GET/PUT | `/system/settings` |
| POST | `/system/backup`, `/system/restore` |
| GET/POST/PUT | `/users`, `/users/{user_id}` |

---

## 4. Event mới

### Event types (v1.8.1 catalog)

| event_type | Classification | Severity |
|------------|----------------|----------|
| `UNIFORM_VIOLATION` | BIOSECURITY | MEDIUM |
| `ZONE_INTRUSION` | BIOSECURITY | HIGH |
| `NO_HAND_SANITIZATION` | BIOSECURITY | HIGH |
| `NO_BOOT_SANITIZATION` | BIOSECURITY | HIGH |
| `BIOSECURITY_PROCESS_VIOLATION` | BIOSECURITY | CRITICAL |
| `ANIMAL_INTRUSION` | ANIMAL | HIGH |
| `VEHICLE_INTRUSION` | VEHICLE | HIGH |
| `CAMERA_OFFLINE` | SYSTEM | MEDIUM |

**Category DB:** `compliance_violation`, `workflow_violation`

### Event bus topics (không đổi v1.7)

- `observation.created` → pipeline
- `track.updated` → zone/compliance
- `event.created` → WebSocket
- `camera.status` → health

---

## 5. Component frontend mới

### `src/components/compliance/`

- `ComplianceEventCard.jsx`
- `ComplianceFilters.jsx`
- `ComplianceSummary.jsx`
- `EvidenceSnapshotModal.jsx`

### `src/components/dashboard/`

- `ComplianceKpiWidgets.jsx`
- `TopViolationsWidget.jsx`
- `CameraHealthWidget.jsx`

---

## 6. Route frontend mới

| Path | Page |
|------|------|
| `/monitoring/compliance-center` | ComplianceCenterPage |
| `/setup` | SetupWizardPage |
| `/system-status` | SystemStatusPage |
| `/diagnostics` | DiagnosticsPage |
| `/evidence` | SnapshotBrowserPage |

---

## 7. Phát hiện trong audit

| # | Issue | Trạng thái |
|---|-------|-----------|
| 1 | `reports.py` thiếu `router = APIRouter(...)` — app không import được | **Đã sửa** |
| 2 | Uniform API không có DELETE | Known gap — ghi PARTIALLY READY |
| 3 | Backend yêu cầu Python 3.11+; venv local 3.9.6 | Env note — không sửa code |
| 4 | JS ruleRegistry thiếu BiosecurityProcessRule vs Python | Mirror drift — không ảnh hưởng runtime Python |

---

## 8. Test coverage liên quan

| Test file | Phạm vi |
|-----------|---------|
| `test_compliance_framework.py` | Engine, rules, zone intrusion |
| `test_compliance_phase3.py` | UniformRule |
| `test_biosecurity_workflow.py` | Workflow engine, integration |
| `test_event_catalog_v181.py` | Catalog, KPIs |
| `test_demo_event_generator.py` | Demo mode |

**Kết quả:** 76 backend tests passed · 51 frontend tests passed
