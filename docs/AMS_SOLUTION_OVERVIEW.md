# AMS — Solution Overview

Tài liệu mô tả giải pháp AMS (Animal Management System) phiên bản **v2.0**, dành cho đội kỹ thuật, vận hành và đối tác tích hợp.

---

## 1. Tổng quan giải pháp

AMS là hệ thống giám sát **tuân thủ an toàn sinh học (ATSH)** trên nền camera IP, kết hợp:

1. **Ingest video** — RTSP từ camera (FFmpeg)
2. **Phân tích sự kiện** — pipeline quan sát → rule/compliance → event
3. **Realtime** — WebSocket broadcast tới dashboard
4. **Evidence** — snapshot JPEG gắn với từng vi phạm
5. **Quản trị** — multi-farm, RBAC, audit, backup

AMS **không thay thế** hệ thống ERP/trại; AMS bổ sung lớp **giám sát visual compliance** và cảnh báo vận hành.

---

## 2. Phạm vi chức năng

### 2.1 Compliance Engine

| Rule ID | Mô tả | Phân loại |
|---------|--------|-----------|
| `UNIFORM_VIOLATION` | Sai đồng phục bảo hộ | BIOSECURITY |
| `ZONE_INTRUSION` | Xâm nhập vùng cấm | BIOSECURITY |
| `ANIMAL_INTRUSION` | Động vật xâm nhập | ANIMAL |
| `VEHICLE_INTRUSION` | Xe chưa sát trùng / xâm nhập | VEHICLE |
| `BIOSECURITY_PROCESS_VIOLATION` | Bỏ bước quy trình ATSH | BIOSECURITY |
| `NO_HAND_SANITIZATION` | Không rửa tay sát trùng | BIOSECURITY |
| `NO_BOOT_SANITIZATION` | Không sát trùng ủng | BIOSECURITY |

Mỗi event được enrich: **classification**, **severity**, **title**, **description**, **recommendedAction**.

### 2.2 Biosecurity Workflow Engine (v1.8+)

Quy trình nhiều bước (nhà tắm → rửa tay → sát trùng ủng → vào vùng sản xuất). Workflow timeout cấu hình qua system settings.

### 2.3 Deployment Kit (v2.0)

| Module | Route / API | Mục đích |
|--------|-------------|----------|
| Setup Wizard | `/setup` | Cài đặt Farm → Camera → Zone → Uniform → Check |
| System Status | `/system-status` | KPI vận hành (camera, RTSP, CPU, RAM, GPU) |
| Diagnostics | `/diagnostics` | Disk, network, test zone/rule, export/import |
| Evidence Browser | `/evidence` | Duyệt snapshot theo filter |
| Health API | `GET /api/health` | database, websocket, storage, camera, ffmpeg |

### 2.4 Demo Mode

Khi `DEMO_MODE=true`:

- Không cần camera thật / RTSP / AI model đầy đủ
- `DemoEventGenerator` sinh event compliance định kỳ
- Event đi qua **EventBus → WebSocket** giống production
- Farm demo: **Mind Farm Demo** (3 camera)
- Compliance score dashboard: 85% / 90% / 95% (xoay vòng)

---

## 3. Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (Vite)                      │
│  Dashboard · Compliance Center · Zone Designer · Settings   │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST + WebSocket (/ws/events)
┌───────────────────────────▼─────────────────────────────────┐
│                   FastAPI Backend (app/)                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │ Event Bus   │→ │ Pipeline     │→ │ Compliance Engine   │ │
│  │ InMemory    │  │ Subscribers  │  │ + Workflow Manager  │ │
│  └─────────────┘  └──────────────┘  └─────────────────────┘ │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │ Deployment  │  │ Demo Mode    │  │ Reports / Audit     │ │
│  │ Services    │  │ Generator    │  │ Backup / Retention  │ │
│  └─────────────┘  └──────────────┘  └─────────────────────┘ │
└───────────┬─────────────────────┬───────────────────────────┘
            │                     │
     PostgreSQL              Redis (JWT)
            │
     uploads/ · storage/ · demo-assets/
```

### Event pipeline (production)

```
Observation (detector/RTSP)
    → OBSERVATION_CREATED
    → pipeline_subscribers (zone mapping, track store)
    → ComplianceEngine.evaluate()
    → create_compliance_violation_event(publish=True)
    → EVENT_CREATED
    → EventStreamService → /ws/events
    → Frontend EventStore → Dashboard
```

---

## 4. Multi-farm & bảo mật

### Tenancy

```
Farm
 ├── Users (farm_id + role)
 ├── Cameras → CameraZones → ZoneRules
 ├── Events (farm_id)
 ├── Workflows
 └── UniformTemplates
```

### RBAC

| Role | Quyền |
|------|-------|
| `SUPER_ADMIN` | Toàn hệ thống, backup/restore, import config |
| `FARM_ADMIN` | Quản lý farm được gán: camera, zone, settings |
| `VIEWER` | Chỉ đọc dashboard, events, reports |

JWT: `sub`, `role`, `jti`, `exp` — Redis blacklist khi logout.

### Audit

Mọi thao tác quan trọng (settings, backup, restore) ghi `audit_logs`.

---

## 5. Tích hợp & API

### REST (prefix `/api`)

- Auth: `POST /auth/login`
- Events: `GET /events`
- Compliance reports: `GET /reports/compliance/kpis`
- Deployment: `GET /deployment/status`, `GET /deployment/diagnostics`
- Demo: `POST /demo/start`, `POST /demo/stop`

### WebSocket

- `GET /ws/events` — stream `event.created`, notifications

### Static

- `/uploads` — evidence snapshots
- `/demo-assets` — ảnh demo (person, animal, vehicle, uniform)

Chi tiết API: xem [AMS_API_REFERENCE.md](../AMS_API_REFERENCE.md) ở repo root.

---

## 6. Stack công nghệ

| Layer | Technology |
|-------|------------|
| Frontend | React 18, Vite, React Router |
| Backend | Python 3.11+, FastAPI, SQLAlchemy |
| Database | PostgreSQL 14+ |
| Cache | Redis 6+ |
| Video | FFmpeg / FFprobe (RTSP) |
| Realtime | WebSocket (native) |

---

## 7. Phân biệt môi trường

| Môi trường | Mục đích | Ghi chú |
|------------|----------|---------|
| **Demo** | Sales, training | `DEMO_MODE=true`, Mind Farm Demo |
| **Pilot** | 1 trại thật, 3–9 camera | Setup Wizard, test zone trước go-live |
| **Production** | Multi-farm vận hành | `DEMO_MODE=false`, HTTPS, backup DB |

---

## 8. Roadmap đã hoàn thành (version map)

| Version | Focus |
|---------|-------|
| v1.7 | Compliance framework |
| v1.8 | Biosecurity Workflow Engine |
| v1.8.1 | Event classification, reports, KPI dashboard |
| v1.9 RC1 | Multi-farm, RBAC, audit, backup |
| v2.0 | Deployment Kit, Demo Mode, diagnostics |

---

## 9. Tài liệu liên quan

- [AMS_DEPLOYMENT_GUIDE.md](./AMS_DEPLOYMENT_GUIDE.md)
- [AMS_SYSTEM_ARCHITECTURE.md](../AMS_SYSTEM_ARCHITECTURE.md)
- [INSTALL.md](../INSTALL.md) · [QUICK_START.md](../QUICK_START.md)
- [CAMERA_SETUP.md](../CAMERA_SETUP.md) · [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
