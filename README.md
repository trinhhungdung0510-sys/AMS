# AMS — Animal Management System

Giám sát an toàn sinh học (ATSH) trên camera IP — dashboard realtime, compliance engine, multi-farm RBAC.

---

## Requirements

| Component | Version |
|-----------|---------|
| **Python (backend)** | **3.11+** |
| Node.js (frontend) | 18+ |
| PostgreSQL | 14+ |
| Redis | 6+ |
| FFmpeg | 4.4+ (production, RTSP) |

> **Required Python Version = 3.11+**  
> Backend **không chạy** trên Python 3.9/3.10 nếu thiếu cú pháp PEP 604. Chi tiết: [PYTHON_RUNTIME_REQUIREMENTS.md](./PYTHON_RUNTIME_REQUIREMENTS.md)

---

## Quick Start

```bash
# Backend (Python 3.11+)
cd backend
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head && python scripts/seed.py
uvicorn app.main:app --port 8000

# Frontend
cd ..
npm install && npm run dev
```

Mở http://localhost:5173 — `admin@ams.local` / `admin123`

Hướng dẫn đầy đủ: [INSTALL.md](./INSTALL.md) · [QUICK_START.md](./QUICK_START.md)

---

## Project Structure

```
AMS/
├── backend/          # FastAPI (Python 3.11+)
│   └── app/          # API, compliance, workflow, services
├── src/              # React + Vite frontend
├── docs/             # Brochure, deployment, pilot, pricing
└── scripts/          # deploymentCheck.js
```

---

## Documentation

| Doc | Mục đích |
|-----|----------|
| [INSTALL.md](./INSTALL.md) | Cài đặt |
| [PYTHON_RUNTIME_REQUIREMENTS.md](./PYTHON_RUNTIME_REQUIREMENTS.md) | Yêu cầu Python & cú pháp 3.10+ |
| [docs/AMS_SOLUTION_OVERVIEW.md](./docs/AMS_SOLUTION_OVERVIEW.md) | Tổng quan giải pháp |
| [docs/AMS_DEPLOYMENT_GUIDE.md](./docs/AMS_DEPLOYMENT_GUIDE.md) | Triển khai |
| [AMS_PRODUCTION_READINESS.md](./AMS_PRODUCTION_READINESS.md) | Production readiness |

---

## Build

```bash
# Frontend
npm run build

# Backend tests
cd backend && pytest tests/ -q
```

---

## Demo Mode

```env
# backend/.env
DEMO_MODE=true
```

Không cần camera thật — event realtime qua WebSocket. Xem Settings → Demo mode.

---

## License

Proprietary — AMS internal deployment.
