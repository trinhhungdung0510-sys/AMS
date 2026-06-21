# AMS v2.0 — Installation Guide

## Required Python Version

**Python 3.11+** (bắt buộc cho backend)

Backend sử dụng cú pháp PEP 604 (`str | None`, `list[str]`, …) được evaluate lúc import trên nhiều module API. Python 3.9 sẽ lỗi `TypeError` khi khởi động server.

```bash
python3.11 --version   # phải >= 3.11
python3.11 -m venv .venv
```

Chi tiết quét toàn bộ codebase: [PYTHON_RUNTIME_REQUIREMENTS.md](./PYTHON_RUNTIME_REQUIREMENTS.md)

---

## Overview

AMS v2.0 Deployment Kit tập trung cài đặt, cấu hình và vận hành. Không thêm AI, detector hay workflow mới.

## Requirements

| Component | Version |
|-----------|---------|
| **Python** | **3.11+** (required) |
| Node.js | 18+ |
| PostgreSQL | 14+ |
| Redis | 6+ |
| FFmpeg | 4.4+ (RTSP ingest) |

## 1. Clone & Dependencies

```bash
git clone <repo-url> ams
cd ams

# Backend
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ..
npm install
```

## 2. Environment

Tạo `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://ams:ams_password@localhost:5432/ams
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=change-me-in-production
CORS_ORIGINS=http://localhost:5173
UPLOADS_ROOT=./uploads
STORAGE_ROOT=./storage
FFMPEG_PATH=ffmpeg
FFPROBE_PATH=ffprobe
```

Tạo `.env` ở root frontend:

```env
VITE_API_URL=http://localhost:8000
```

## 3. Database

```bash
cd backend
alembic upgrade head
python scripts/seed.py
```

## 4. Start Services

```bash
# Terminal 1 — Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2 — Frontend
npm run dev
```

Production build:

```bash
npm run build
# Serve dist/ với nginx hoặc static host
```

## 5. Setup Wizard

Sau khi đăng nhập với tài khoản SUPER_ADMIN:

1. Mở **Setup Wizard** (`/setup`)
2. Tạo Farm → Camera → Zone → Uniform
3. Chạy **Kiểm tra hệ thống** (bước 5)

## 6. Health & Diagnostics

```bash
# Public health API
curl http://localhost:8000/api/health

# Deployment readiness
node scripts/deploymentCheck.js http://localhost:8000
```

Trong UI:

- **System Status** (`/system-status`) — camera, RTSP, storage, CPU, RAM, GPU
- **Diagnostics** (`/diagnostics`) — disk, network, camera reachability, test zone/rule, export/import

## 7. Default Admin

| Field | Value |
|-------|-------|
| Email | admin@ams.local |
| Password | admin123 |
| Role | SUPER_ADMIN |

Đổi mật khẩu ngay trên môi trường production.

## 8. Docker (optional)

```bash
cd backend
docker compose up -d postgres redis
```

Sau đó chạy migration và uvicorn như trên.

## Related Docs

- [PYTHON_RUNTIME_REQUIREMENTS.md](./PYTHON_RUNTIME_REQUIREMENTS.md)
- [QUICK_START.md](./QUICK_START.md)
- [CAMERA_SETUP.md](./CAMERA_SETUP.md)
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- [AMS_RC1_DEPLOYMENT.md](./AMS_RC1_DEPLOYMENT.md)
