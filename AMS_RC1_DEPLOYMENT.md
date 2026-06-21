# AMS v1.9 RC1 — Deployment Guide

## Overview

AMS v1.9 RC1 chuyển hệ thống từ prototype sang product-ready với multi-farm, RBAC, audit log, system settings, backup/restore và retention job.

## Requirements

| Component | Version |
|-----------|---------|
| Python | 3.11+ |
| Node.js | 18+ |
| PostgreSQL | 14+ |
| Redis | 6+ |

## Environment Variables

Tạo `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://ams:ams_password@localhost:5432/ams
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=change-me-in-production
CORS_ORIGINS=http://localhost:5173

# Compliance & system
COMPLIANCE_UNIFORM_THRESHOLD=0.85
DEMO_MODE=false
DEMO_SEED_ON_STARTUP=false
WORKFLOW_TIMEOUT_SECONDS=300
RETENTION_DAYS=90
```

Frontend `.env`:

```env
VITE_API_URL=http://localhost:8000
```

## Database Migration

```bash
cd backend
alembic upgrade head
python scripts/seed.py
```

Migration mới: `0034_v19_rc1_multi_farm_rbac`

## Start Services

```bash
# Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend
npm run dev
```

## Default Admin

| Field | Value |
|-------|-------|
| Email | admin@ams.local |
| Password | admin123 |
| Role | SUPER_ADMIN |
| Farm | FARM-001 |

**Đổi mật khẩu ngay sau khi deploy production.**

## Deployment Check

```bash
node scripts/deploymentCheck.js http://localhost:8000
```

Kiểm tra: Database, Uploads folder, WebSocket endpoint, Config file, Memory.

## Backup Before Go-Live

```bash
curl -X POST http://localhost:8000/api/system/backup \
  -H "Authorization: Bearer $TOKEN" \
  -o ams-backup.json
```

## Production Checklist

- [ ] `JWT_SECRET_KEY` mạnh, không dùng default
- [ ] `DEMO_MODE=false`
- [ ] PostgreSQL backup tự động (ngoài AMS JSON backup)
- [ ] HTTPS reverse proxy (nginx/Caddy)
- [ ] CORS chỉ allow domain production
- [ ] Retention days phù hợp chính sách lưu trữ
- [ ] Tạo FARM_ADMIN per farm, hạn chế SUPER_ADMIN

## Docker (optional)

Nếu dùng docker-compose có sẵn trong repo, chạy:

```bash
docker compose up -d postgres redis
cd backend && alembic upgrade head && python scripts/seed.py
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 401 on API | Login lại, kiểm tra JWT secret |
| 403 on settings | User cần FARM_ADMIN+ |
| Migration fail | `alembic current` → upgrade từ 0033 |
| WS không realtime | Kiểm tra `/ws/events` qua deploymentCheck |
