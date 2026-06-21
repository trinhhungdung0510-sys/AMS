# AMS API Reference — v1.9 RC1

Base URL: `/api`  
Auth: `Authorization: Bearer <token>`

## Auth

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/login` | Login → JWT |
| POST | `/auth/logout` | Revoke token |
| GET | `/auth/me` | Current user + role + farm_id |

## Farms

| Method | Path | Role | Description |
|--------|------|------|-------------|
| GET | `/farms` | All | List farms (scoped) |
| GET | `/farms/{id}` | All | Farm detail |
| POST | `/farms` | SUPER_ADMIN | Create farm |
| PUT | `/farms/{id}` | SUPER_ADMIN / FARM_ADMIN | Update farm |

**Farm model fields:** `id`, `name`, `code`, `address`, `contactName`, `contactPhone`, `createdAt`

## Users

| Method | Path | Role | Description |
|--------|------|------|-------------|
| GET | `/users?farm_id=` | FARM_ADMIN+ | List users |
| POST | `/users` | FARM_ADMIN+ | Create user |
| PUT | `/users/{id}` | FARM_ADMIN+ | Update user |

**Roles:** `SUPER_ADMIN`, `FARM_ADMIN`, `VIEWER`

## Cameras / Zones / Workflows

Tất cả scoped theo `farm_id`. Camera và Event đã có `farm_id`; Workflow, Uniform, CameraZone thêm từ v1.9.

| Resource | farm_id |
|----------|---------|
| Camera | direct |
| Event | direct |
| CameraZone | direct |
| Workflow | direct |
| UniformTemplate | direct |
| Compliance events | via camera/event |

## System Settings

| Method | Path | Description |
|--------|------|-------------|
| GET | `/system/settings` | Read settings |
| PUT | `/system/settings` | Update settings |

**Settings keys:**

```json
{
  "compliance_threshold": 0.85,
  "workflow_timeout": 300,
  "demo_mode": false,
  "retention_days": 90
}
```

## Backup / Restore

| Method | Path | Role | Description |
|--------|------|------|-------------|
| POST | `/system/backup` | FARM_ADMIN+ | Export JSON |
| POST | `/system/restore` | SUPER_ADMIN | Restore config |

**Backup includes:** farms, cameras, zones, workflows, uniforms, settings

## Audit Log

| Method | Path | Description |
|--------|------|-------------|
| GET | `/audit?farm_id=&action=&limit=` | List audit entries |

**Audited actions:** `login`, `logout`, `create_zone`, `delete_zone`, `update_camera`, `update_uniform`, `update_workflow`, `update_settings`, `create_backup`, `restore_backup`

## Uniforms

| Method | Path | Description |
|--------|------|-------------|
| GET | `/uniforms` | List uniform templates |
| POST | `/uniforms` | Create template |
| PUT | `/uniforms/{id}` | Update template |

## Reports (v1.8.1)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/reports/compliance` | Today / 7d / 30d summary |
| GET | `/reports/compliance/kpis` | Dashboard KPIs |
| GET | `/reports/compliance/top-violations` | Top 10 violations |
| GET | `/reports/compliance/pdf-data` | PDF data structure |

## Health

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | No | DB + Redis status |

## WebSocket

| Path | Events |
|------|--------|
| `/ws/events` | `event.created`, compliance violations |
| `/ws/dashboard` | Dashboard updates |

## Error Codes

| Code | Meaning |
|------|---------|
| 401 | Invalid/expired token |
| 403 | Missing permission or farm access |
| 404 | Resource not found |
| 409 | Duplicate ID/email |
