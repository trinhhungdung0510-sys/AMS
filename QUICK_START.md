# AMS v2.0 — Quick Start

Triển khai AMS trong 1 ngày với Setup Wizard.

## 15-Minute Local Setup

**Một lệnh (khuyến nghị):**

```bash
npm run dev:local
```

Script tự: bật Docker · tạo `.env` nếu thiếu · cài venv nếu thiếu · chạy backend + frontend · mở trình duyệt.

Dừng: `npm run dev:stop`

---

**Thủ công (2 terminal):**

```bash
# 1. Backend
cd backend && docker compose up -d && ./scripts/start_backend.sh

# 2. Frontend
npm run dev
```

Mở http://localhost:5173 — đăng nhập `admin@ams.local` / `admin123`.

## Setup Wizard (5 bước)

| Bước | Hành động | Mục tiêu |
|------|-----------|----------|
| 1 | Tạo Farm | Gán tenant / trại |
| 2 | Thêm Camera | RTSP URL, IP, zone label |
| 3 | Tạo Zone | Polygon trên camera |
| 4 | Gán Uniform | Template đồng phục |
| 5 | Kiểm tra hệ thống | DB, storage, camera, ffmpeg |

Route: `/setup`

## Verify Deployment

```bash
node scripts/deploymentCheck.js http://localhost:8000
curl http://localhost:8000/api/health | jq
```

Kỳ vọng `status`: `ok` hoặc `degraded` (một số camera offline vẫn chấp nhận được).

## Daily Operations

| Page | Route | Use case |
|------|-------|----------|
| System Status | `/system-status` | Theo dõi camera online/offline, RTSP, tài nguyên |
| Diagnostics | `/diagnostics` | Test zone/rule, export/import config |
| Evidence | `/evidence` | Duyệt snapshot theo farm/camera/ngày/rule |
| Settings | `/settings` | RBAC, backup (v1.9) |

## Export / Import Config

**Export** (Diagnostics page hoặc API):

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/deployment/export -o ams-config-bundle.json
```

Bundle gồm: `farm.json`, `camera.json`, `zone.json`, `workflow.json`, `settings.json`, `uniform.json`.

**Import** — SUPER_ADMIN only, qua Diagnostics UI hoặc:

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @ams-config-bundle.json \
  http://localhost:8000/api/deployment/import
```

## Go-Live Checklist

- [ ] Đổi mật khẩu admin
- [ ] Setup Wizard hoàn tất 5/5 bước
- [ ] `/api/health` trả về ok/degraded
- [ ] Test Zone trên từng camera quan trọng
- [ ] Test Compliance Rule với rule thực tế
- [ ] Export config backup trước go-live
- [ ] FFmpeg có trên PATH server

## Next Steps

- [CAMERA_SETUP.md](./CAMERA_SETUP.md) — cấu hình RTSP chi tiết
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) — xử lý sự cố thường gặp
