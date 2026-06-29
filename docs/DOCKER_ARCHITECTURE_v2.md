# Docker Architecture v2 — AMS Backend API

AMS v1.7 dockerizes the Backend API alongside Postgres, Redis, and AMS Vision on a single Docker network.

## Services

| Service | Container | Port | Image / Build |
|---------|-----------|------|----------------|
| `postgres` | `ams-postgres` | 5432 | `postgres:16-alpine` |
| `redis` | `ams-redis` | 6379 | `redis:7-alpine` |
| `backend` | `ams-backend` | 8000 | `./backend/Dockerfile` |
| `ams-vision` | `ams-vision` | 8010 | `../ams-vision/Dockerfile` |

All services attach to network **`ams-net`**. Internal DNS uses Compose service names (`postgres`, `redis`, `backend`, `ams-vision`).

## Architecture

```
┌─────────────┐     HTTP      ┌──────────────┐
│  ams-vision │──────────────▶│   backend    │
│   :8010     │ backend:8000  │    :8000     │
└─────────────┘               └──────┬───────┘
                                     │
                        ┌────────────┼────────────┐
                        ▼            ▼            │
                   postgres      redis          │
                   :5432        :6379           │
                        └────────────┴────────────┘
                              ams-net
```

Frontend (host, `:5173`) calls `http://127.0.0.1:8000/api/*` — Backend is published on host port 8000.

Vision publishes observations to `http://backend:8000` (Docker network, not `host.docker.internal`).

### Port 8000 — tránh trùng backend

Chỉ **một** process được phục vụ `:8000` trên máy host:

| Process | Nhận biết qua `/api/health` → `ffmpeg` |
|---------|----------------------------------------|
| Docker `ams-backend` | `/usr/bin/ffmpeg` |
| uvicorn local (`.venv`) | `/opt/homebrew/bin/ffmpeg` (macOS) |

`npm run dev:local` sau AMS v1.7: Docker Compose đã gồm `backend` → script **không** khởi động uvicorn local nếu `ams-backend` healthy. Nếu vẫn lỗi Gmail «Thiếu SMTP_USER», kiểm tra:

```bash
curl -s http://127.0.0.1:8000/api/health | jq .ffmpeg.ffmpeg
# Phải là /usr/bin/ffmpeg khi dùng Docker backend

npm run dev:stop   # dừng uvicorn local, giữ Docker
```

## Backend service

**Build context:** `backend/`

**Configuration:**
- `env_file: .env` — SMTP, JWT, CORS, Zalo, etc.
- Compose overrides for Docker network:
  - `DATABASE_URL=postgresql+psycopg://ams:ams_password@postgres:5432/ams`
  - `REDIS_URL=redis://redis:6379/0`

**Volumes:**
- `.:/app` — live source mount (uvicorn `--reload`)
- `backend_uploads`, `backend_storage` — persistent uploads/storage

**Startup (`docker-entrypoint.sh`):**
1. Wait for Postgres
2. `alembic upgrade head`
3. `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

**Healthcheck:** `GET /api/health` inside container

## Quick start

```bash
cd backend
cp .env.example .env   # chỉnh SMTP_USER, SMTP_PASSWORD nếu cần Gmail
npm run dev:up         # khuyến nghị: Docker + frontend web cùng lúc
# hoặc: bash scripts/up.sh
docker compose ps
```

Expected `docker compose ps`:

```
NAME           SERVICE      STATUS
ams-backend    backend      running (healthy)
ams-postgres   postgres     running (healthy)
ams-redis      redis        running (healthy)
ams-vision     ams-vision   running
```

### Seed data (first run)

Admin user is created by seed script, not migrations:

```bash
docker compose exec backend python scripts/seed.py
```

Login: `admin@ams.local` / `admin123`

## Verification

```bash
# Health
curl -s http://127.0.0.1:8000/api/health | jq .

# Login
curl -s -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ams.local","password":"admin123"}' | jq .

# Gmail connect (requires SMTP in backend/.env)
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ams.local","password":"admin123"}' | jq -r .access_token)

curl -s -X POST http://127.0.0.1:8000/api/notification/gmail/connect \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"gmail_recipient":"your@gmail.com"}' | jq .
```

## SMTP from `.env`

Notification Service reads SMTP only from `backend/.env` inside the container:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-sender@gmail.com
SMTP_PASSWORD=your-google-app-password
```

No change to Rule Engine, Compliance Engine, Workflow Engine, or Notification Service logic — only deployment packaging.

## Vision configuration

```yaml
ams-vision:
  environment:
    BACKEND_BASE_URL: http://backend:8000
```

Removed: `host.docker.internal`, `extra_hosts`.

## Files

| File | Purpose |
|------|---------|
| `backend/Dockerfile` | Python 3.12 API image |
| `backend/docker-entrypoint.sh` | Migrate + start uvicorn |
| `backend/docker-compose.yml` | Full stack compose |
| `backend/.dockerignore` | Exclude venv, caches |

## Stop / reset

```bash
cd backend
docker compose down
docker compose down -v   # xóa volumes (DB reset)
```
