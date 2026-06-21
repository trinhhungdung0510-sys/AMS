# AMS System Architecture — v1.9 RC1

## High-Level

```
┌─────────────┐     REST/WS      ┌──────────────────┐
│  React UI   │ ◄──────────────► │  FastAPI Backend │
│  (Vite)     │                  │  app/main.py     │
└─────────────┘                  └────────┬─────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    ▼                     ▼                     ▼
              PostgreSQL              Redis              uploads/
              (events, farms,         (JWT blacklist)    evidence/
               users, audit)
```

## Multi-Farm Tenancy

```
Farm (FARM-001, FARM-002, ...)
  ├── Users (farm_id + role)
  ├── Cameras (farm_id)
  │     └── CameraZones (farm_id)
  ├── Events (farm_id)
  ├── Workflows (farm_id)
  └── UniformTemplates (farm_id)
```

**Backward compatibility:** Dữ liệu cũ không có `farm_id` → migration gán `FARM-001`.

**Scoping:** `resolve_farm_scope()` trong `app/core/farm_access.py` — SUPER_ADMIN thấy tất cả; FARM_ADMIN/VIEWER chỉ farm được gán.

## RBAC

```
SUPER_ADMIN  →  permission "*"
FARM_ADMIN   →  manage cameras, zones, workflows, uniforms, settings (own farm)
VIEWER       →  read-only
```

Implementation:
- `app/core/roles.py` — role constants, permission map
- `app/core/permissions.py` — `require_permission()` FastAPI dependency
- JWT payload: `sub`, `role`, `jti`, `exp`

## Event Pipeline (unchanged core)

```
Observation → EventBus → pipeline_subscribers
                              ├── Rule evaluation
                              ├── Compliance (UniformRule)
                              └── Biosecurity Workflow Engine
                                        ↓
                              create_compliance_violation_event
                                        ↓
                              event_to_engine_dict (+ classification v1.8.1)
                                        ↓
                              /ws/events → Frontend EventStore
```

## Audit Trail

```
User action → write_audit_log() → audit_logs table
```

Fields: `farm_id`, `user_id`, `action`, `resource_type`, `resource_id`, `metadata_json`, `created_at`

## System Settings

Persisted in `system_settings` table, merged with env defaults from `app/core/config.py`.

Used by:
- Compliance threshold → UniformRule
- Retention days → background retention worker
- Demo mode → demo API + seed
- Workflow timeout → workflow engine (config ready)

## Background Jobs

| Worker | Interval | File |
|--------|----------|------|
| Camera health | 30s | `main.py` |
| RTSP simulator | continuous | `rtsp_simulator.py` |
| Event retention | 6h | `retention_service.py` |

## Backup / Restore

```
POST /system/backup  → backup_service.export_backup()
POST /system/restore → backup_service.restore_backup()
```

JSON-only — không backup events (tránh file quá lớn). Events được quản lý bởi retention policy.

## Frontend Modules

| Page | Path | API |
|------|------|-----|
| Dashboard | `/dashboard` | reports, camera-health |
| Compliance Center | `/monitoring/compliance-center` | compliance events |
| Settings | `/settings` | system, users, cameras |
| Zone Designer | `/thiet-ke-vung-atsh` | zones |

## Version Map

| Version | Focus |
|---------|-------|
| v1.7 | Compliance framework |
| v1.7.1 | Evidence Center |
| v1.8 | Biosecurity Workflow Engine |
| v1.8.1 | Event classification, reports, demo mode |
| v1.9 RC1 | Multi-farm, RBAC, audit, deployment |

## Key Directories

```
backend/app/
  api/          REST routers
  core/         config, roles, permissions, farm_access
  models/       SQLAlchemy models
  services/     business logic
  compliance/   compliance engine
  biosecurity_workflow/  workflow engine v1.8
  events/       event catalog v1.8.1

src/
  pages/        React pages
  services/     API clients
  components/   UI widgets
```
