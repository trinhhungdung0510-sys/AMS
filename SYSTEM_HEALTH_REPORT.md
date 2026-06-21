# AMS System Health Report

**Ngày kiểm tra:** 2026-06-18  
**Loại:** Post-implementation validation (static + automated tests)

---

## Executive Summary

| Area | Status | Notes |
|------|--------|-------|
| Backend | **PASS** | 76/76 pytest, compile OK |
| Frontend | **PASS** | build OK, 51/51 vitest |
| WebSocket | **PASS** | client tests + code review |
| Database | **PARTIAL** | migrations present; live DB not running in CI env |
| Storage | **PASS** | paths configured, evidence layout validated |
| Compliance | **PASS** | engine + rules tested |
| Workflow | **PASS** | engine tests pass |
| Demo Mode | **PASS** | generator tests pass |

---

## 1. Backend Status

### Build / test

```text
python -m compileall app -q     → OK
pytest tests/ -q                → 76 passed in 0.53s
```

### Import verification

| Module | Result |
|--------|--------|
| `app.api.reports` | OK (4 routes) — fixed missing router |
| `app.compliance.compliance_engine` | OK |
| `app.biosecurity_workflow.workflow_engine` | OK |

### Environment note

- **Yêu cầu:** Python 3.11+
- **Venv local:** Python 3.9.6 — `from app.main import app` fails on `str | None` syntax
- **Khuyến nghị production:** dùng Python 3.11+ trước go-live

### Backend npm

Không có `package.json` trong `backend/` — validation backend = **pytest + compileall** (không phải npm build).

---

## 2. Frontend Status

### Build

```text
npm install  → OK
npm run build → ✓ built in ~550ms
  dist/index.html
  dist/assets/index-*.css (~91 KB)
  dist/assets/index-*.js (~851 KB)
```

### Tests

```text
npm test → 10 files, 51 tests passed
  wsClient.test.js (2)
  eventNormalizer.test.js (7)
  eventStoreFlow.test.js (4)
  ...
```

### Warnings

- Chunk size > 500 KB — informational only, không block build

---

## 3. WebSocket Status

### Server

- Endpoint: `GET /ws/events` (`backend/app/ws/event_gateway.py`)
- Bridge: `event_stream_service.py` forwards `EVENT_CREATED` → `events_manager.broadcast`

### Client

- `src/services/wsClient.js` — exponential backoff reconnect (3s → 30s max)
- Singleton shared client — tránh duplicate connections
- Consumers: `EventStore.jsx`, `ComplianceCenterPage.jsx`, `useRealtimeEvents.js`

### Validation

| Check | Method | Result |
|-------|--------|--------|
| URL construction | unit test | PASS |
| Reconnect backoff | code review | PASS |
| Listener error isolation | try/catch per listener | PASS |
| Disconnect on unmount | EventStore cleanup | PASS |

**Live WS test:** cần backend running + browser — không chạy trong CI env này.

---

## 4. Database Status

### Migrations

34 migration files trong `backend/alembic/versions/`

Key migrations:

| Version | File | Content |
|---------|------|---------|
| v1.7 | `0033_compliance_uniform_v17.py` | uniform_templates |
| v1.9 | `0034_v19_rc1_multi_farm_rbac.py` | farm_id, RBAC, audit |

### Schema entities validated (models exist)

| Entity | Model | FK |
|--------|-------|-----|
| Camera | `models/camera.py` | farm_id |
| Zone | `models/camera_zone.py` | camera_id, farm_id |
| Event | `models/event.py` | farm_id, camera_id |
| UniformTemplate | `models/uniform_template.py` | farm_id |
| Workflow | `models/workflow.py` | farm_id |
| Farm | `models/farm.py` | — |
| SystemSetting | `models/system_setting.py` | — |

### Live migration

```text
alembic current → FAILED (PostgreSQL not running on localhost:5432)
```

**Khuyến nghị:** chạy `alembic upgrade head` trên môi trường có Postgres trước demo khách.

### Orphan data

Không kiểm tra runtime (no DB). Code review: events reference `camera_id`, `farm_id` — seed script dùng merge idempotent.

---

## 5. Storage Status

| Path | Purpose | Config |
|------|---------|--------|
| `uploads/` | Evidence snapshots | `UPLOADS_ROOT` |
| `uploads/evidence/YYYY/MM/DD/` | Compliance JPEG | `COMPLIANCE_EVIDENCE_SUBDIR` |
| `storage/` | Employee assets | `STORAGE_ROOT` |
| `demo-assets/` | Demo snapshots | `DEMO_ASSETS_DIR` |

### Evidence path format

`save_evidence_snapshot()` → `/uploads/evidence/{YYYY}/{MM}/{DD}/event_{timestamp}.jpg`

**Validation:** code review + `evidence_snapshot.py` — PASS

---

## 6. Compliance Status

| Item | Status |
|------|--------|
| 7 rules registered | PASS |
| Zone intrusion creates event | PASS |
| Uniform rule skeleton | PASS |
| Event catalog enrichment | PASS |
| Reports KPI API | PASS (after router fix) |
| Compliance Center UI | PASS (build) |

Chi tiết: [COMPLIANCE_VALIDATION.md](./COMPLIANCE_VALIDATION.md)

---

## 7. Workflow Status

| Item | Status |
|------|--------|
| Step sequence compliant path | PASS |
| Skip shower → violation | PASS |
| Skip boot → violation | PASS |
| Integration emits compliance event | PASS |
| Dashboard API `/workflows/dashboard` | PASS (registered) |

---

## 8. Demo Mode Status

| Item | Status |
|------|--------|
| `DEMO_MODE` config | PASS |
| DemoEventGenerator | PASS |
| Mind Farm Demo bootstrap | PASS |
| Event publish → WS path | PASS (same as production) |
| `/api/demo/start` / `/stop` | PASS |
| Demo assets (4 JPEG) | PASS |

**Live demo test:** cần `DEMO_MODE=true` + running server.

---

## 9. Uniform Template Status (Phase 8)

| Operation | API | Status |
|-----------|-----|--------|
| Create | POST `/uniforms` | PASS |
| Read list | GET `/uniforms` | PASS |
| Update | PUT `/uniforms/{id}` | PASS |
| Delete | — | **NOT IMPLEMENTED** |
| Upload images | `image_paths` in payload | PASS (path strings) |
| Preview | Frontend modal / storage URL | PASS (code review) |
| Zone → Uniform | `CameraZone.required_uniform_id` | PASS (model field) |

---

## 10. Evidence Status (Phase 9)

| Check | Status |
|-------|--------|
| Path pattern YYYY/MM/DD | PASS |
| `snapshot_url` on Event model | PASS |
| `resolveSnapshotUrl()` prepends API_BASE_URL | PASS |
| Evidence browser filter API | PASS |
| Demo snapshots `/demo-assets/*.jpg` | PASS |

---

## 11. Fixes applied during validation

| # | File | Fix |
|---|------|-----|
| 1 | `backend/app/api/reports.py` | Restored `router = APIRouter(prefix="/reports", ...)` removed accidentally |

---

## 12. Commands to reproduce

```bash
# Frontend
cd /path/to/AMS && npm install && npm run build && npm test

# Backend
cd backend && source .venv/bin/activate
python -m compileall app -q
pytest tests/ -q

# Deployment check (needs running server)
node scripts/deploymentCheck.js http://localhost:8000
```

---

**Overall system health:** OPERATIONAL (automated) · **Live infra:** pending Postgres + server start
