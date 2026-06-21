# AMS — Deployment Guide

Hướng dẫn triển khai AMS **v2.0** tại môi trường development, pilot và production. Mục tiêu: **triển khai được trong 1 ngày** với Setup Wizard và deployment check tự động.

---

## 1. Yêu cầu hệ thống

### Phần mềm

| Component | Phiên bản tối thiểu |
|-----------|---------------------|
| Python | 3.11+ |
| Node.js | 18+ |
| PostgreSQL | 14+ |
| Redis | 6+ |
| FFmpeg | 4.4+ (production có camera RTSP) |

### Phần cứng (tham khảo)

| Quy mô | CPU | RAM | Disk | GPU |
|--------|-----|-----|------|-----|
| Pilot (≤9 camera) | 4 core | 8 GB | 100 GB SSD | Optional |
| Production (≤30 camera) | 8+ core | 16 GB | 500 GB SSD | Khuyến nghị NVIDIA |
| Demo only | 2 core | 4 GB | 20 GB | Không cần |

---

## 2. Chuẩn bị môi trường

### 2.1 Clone repository

```bash
git clone <repo-url> ams
cd ams
```

### 2.2 Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 2.3 Frontend

```bash
cd ..   # repo root
npm install
cp .env.example .env 2>/dev/null || true
```

Frontend `.env`:

```env
VITE_API_URL=http://localhost:8000
```

---

## 3. Cấu hình backend (.env)

```env
DATABASE_URL=postgresql+psycopg://ams:ams_password@localhost:5432/ams
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=change-me-in-production
CORS_ORIGINS=http://localhost:5173

UPLOADS_ROOT=uploads
STORAGE_ROOT=storage
FFMPEG_PATH=ffmpeg
FFPROBE_PATH=ffprobe

# Compliance
COMPLIANCE_UNIFORM_THRESHOLD=0.85
RETENTION_DAYS=90
WORKFLOW_TIMEOUT_SECONDS=300

# Demo (tắt trên production)
DEMO_MODE=false
DEMO_AUTO_START=true
DEMO_SEED_ON_STARTUP=true
DEMO_SEED_COUNT=12
DEMO_INTERVAL_SECONDS=20
```

---

## 4. Database & seed

```bash
cd backend

# Docker (optional)
docker compose up -d postgres redis

alembic upgrade head
python scripts/seed.py
```

Tài khoản mặc định sau seed:

| Field | Value |
|-------|-------|
| Email | admin@ams.local |
| Password | admin123 |
| Role | SUPER_ADMIN |

**Đổi mật khẩu ngay trên production.**

---

## 5. Khởi động dịch vụ

### Development

```bash
# Terminal 1 — Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 — Frontend
npm run dev
```

Truy cập: http://localhost:5173

### Production build

```bash
npm run build
# Serve dist/ qua nginx hoặc CDN
```

Backend production (ví dụ gunicorn + uvicorn workers):

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

---

## 6. Setup Wizard (triển khai 1 ngày)

Đăng nhập SUPER_ADMIN → **Setup Wizard** (`/setup`)

| Bước | Hành động | Output |
|------|-----------|--------|
| 1 | Tạo Farm | Tenant / trại mới |
| 2 | Thêm Camera | RTSP URL, IP, credentials |
| 3 | Tạo Zone | Polygon trên camera |
| 4 | Gán Uniform | Template đồng phục theo vùng |
| 5 | Kiểm tra hệ thống | Health: DB, storage, ffmpeg, camera |

---

## 7. Xác minh triển khai

### Deployment check script

```bash
node scripts/deploymentCheck.js http://localhost:8000
```

Kiểm tra: Database, `/api/health`, config, uploads, WebSocket endpoint, memory.

### Health API

```bash
curl http://localhost:8000/api/health | jq
```

Kỳ vọng `status`: `ok` hoặc `degraded` (một số camera offline có thể chấp nhận trong giai đoạn cấu hình).

### Test zone & rule (trước go-live)

1. **Diagnostics** (`/diagnostics`) → Test Zone → xác nhận overlay coordinates
2. Test Compliance Rule → xem input/output/score
3. **System Status** (`/system-status`) → camera online, RTSP/ffmpeg

---

## 8. Export / Import cấu hình

### Export bundle

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/deployment/export \
  -o ams-config-bundle.json
```

Files trong bundle: `farm.json`, `camera.json`, `zone.json`, `workflow.json`, `settings.json`, `uniform.json`.

### Import (SUPER_ADMIN only)

Qua Diagnostics UI hoặc:

```bash
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @ams-config-bundle.json \
  http://localhost:8000/api/deployment/import
```

**Khuyến nghị:** export config backup trước mọi thay đổi lớn.

---

## 9. Production checklist

- [ ] `JWT_SECRET_KEY` mạnh, không dùng default
- [ ] `DEMO_MODE=false`
- [ ] HTTPS reverse proxy (nginx / Caddy / ALB)
- [ ] CORS chỉ allow domain production
- [ ] PostgreSQL backup tự động (ngoài AMS JSON backup)
- [ ] Setup Wizard hoàn tất 5/5 bước
- [ ] Test zone trên từng camera quan trọng
- [ ] FFmpeg có trên PATH server edge
- [ ] Tạo FARM_ADMIN per farm; hạn chế tài khoản SUPER_ADMIN
- [ ] Retention days phù hợp chính sách lưu trữ nội bộ
- [ ] Firewall: server AMS ↔ camera VLAN (port 554 RTSP)

### Backup hệ thống

```bash
curl -X POST http://localhost:8000/api/system/backup \
  -H "Authorization: Bearer $TOKEN" \
  -o ams-backup.json
```

---

## 10. Demo Mode (không production)

Dùng cho sales demo, training, UAT nội bộ:

```env
DEMO_MODE=true
DEMO_AUTO_START=true
```

- Không cần camera / RTSP
- Farm **Mind Farm Demo** tự tạo
- Event sinh realtime qua WebSocket
- Bật/tắt: Settings → Demo mode → Bắt đầu / Dừng Demo

API: `POST /api/demo/start`, `POST /api/demo/stop`

---

## 11. Nginx reverse proxy (mẫu)

```nginx
server {
    listen 443 ssl;
    server_name ams.example.com;

    location / {
        root /var/www/ams/dist;
        try_files $uri /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /uploads {
        proxy_pass http://127.0.0.1:8000;
    }

    location /demo-assets {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

---

## 12. Troubleshooting

| Triệu chứng | Nguyên nhân thường gặp | Xử lý |
|-------------|------------------------|-------|
| 401 API | Token hết hạn | Login lại |
| Camera offline | RTSP sai / firewall | Diagnostics → camera reachability |
| ffmpeg unavailable | Chưa cài FFmpeg | `which ffmpeg` |
| WS không realtime | Proxy thiếu Upgrade | Kiểm tra nginx `/ws/` |
| KPI compliance = 0 | Event không đúng loại/ngày | Bật demo hoặc kiểm tra rule |
| Import 403 | Không phải SUPER_ADMIN | Dùng tài khoản admin |

Chi tiết: [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)

---

## 13. Tài liệu tham chiếu

| File | Nội dung |
|------|----------|
| [INSTALL.md](../INSTALL.md) | Cài đặt chi tiết |
| [QUICK_START.md](../QUICK_START.md) | Quick start 15 phút |
| [CAMERA_SETUP.md](../CAMERA_SETUP.md) | Cấu hình RTSP |
| [AMS_API_REFERENCE.md](../AMS_API_REFERENCE.md) | API đầy đủ |
| [AMS_SYSTEM_ARCHITECTURE.md](../AMS_SYSTEM_ARCHITECTURE.md) | Kiến trúc |
