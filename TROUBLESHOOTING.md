# AMS v2.0 — Troubleshooting

## Health API

```bash
curl http://localhost:8000/api/health
```

| Field | ok | degraded / unavailable | Fix |
|-------|-----|------------------------|-----|
| database | connected | error | Kiểm tra `DATABASE_URL`, postgres đang chạy |
| websocket | ok | — | Restart backend nếu WS không kết nối |
| storage | ok | degraded | Quyền ghi `UPLOADS_ROOT`, `STORAGE_ROOT` |
| camera | ok | degraded | Một phần camera offline — xem Diagnostics |
| ffmpeg | ok | unavailable | Cài ffmpeg/ffprobe, set `FFMPEG_PATH` |

Legacy endpoint vẫn hoạt động: `GET /health` (DB + Redis only).

## Setup Wizard

### Bước 1 — Tạo Farm thất bại

- Cần role **SUPER_ADMIN**
- Farm ID trùng → đổi mã hoặc xóa farm cũ

### Bước 5 — System check failed

- Mở `/diagnostics` xem chi tiết disk/memory/network
- Chạy `node scripts/deploymentCheck.js`

## Camera / RTSP

### Camera Offline trên System Status

1. Ping IP camera từ server AMS
2. Kiểm tra RTSP URL: `rtsp://user:pass@ip:554/stream`
3. Diagnostics → **camera reachability**
4. Xác nhận firewall mở port 554

### FFmpeg unavailable

```bash
which ffmpeg ffprobe
ffmpeg -version
```

Cài package hệ thống hoặc chỉ đường dẫn trong `.env`.

## Zone Test Mode

**Zone không hiển thị overlay**

- Kiểm tra Zone ID đúng (CameraZone hoặc ZonePolygon)
- Coordinates phải là mảng điểm `[{x,y}, ...]` normalized 0–1

API:

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/deployment/zones/{zone_id}/test
```

## Rule Test Mode

**Score luôn 0 hoặc violated=false**

- Rule test là **simulation** — không chạy detector mới
- `UNIFORM_VIOLATION` dùng mock uniform matcher với threshold từ settings
- Kiểm tra `COMPLIANCE_UNIFORM_THRESHOLD` trong `.env`

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ruleType":"UNIFORM_VIOLATION","trackId":101,"score":0.72}' \
  http://localhost:8000/api/deployment/rules/test
```

## Evidence Browser

**Không có snapshot**

- Event phải có `category=compliance_violation` và `snapshot_url`
- Bật demo/seed nếu môi trường dev trống: `DEMO_SEED_ON_STARTUP=true`

## Export / Import

### Import 403

- Chỉ **SUPER_ADMIN** được import

### Import partial failure

- Response `counts` cho biết số bản ghi từng loại
- Kiểm tra JSON hợp lệ, version `"2.0"` trong bundle

## Frontend

### Sidebar "Cần kiểm tra hệ thống"

- `/api/health` không reachable hoặc `status=error`
- Kiểm tra `VITE_API_URL` và CORS

### Build errors

```bash
npm run build
cd backend && python -m compileall app
```

## Logs

```bash
# Backend uvicorn stdout
# Camera health worker — mỗi 30s evaluate statuses
```

## Support Checklist

Thu thập trước khi escalate:

1. Output `curl /api/health`
2. Output `node scripts/deploymentCheck.js`
3. Screenshot System Status + Diagnostics
4. Export config bundle (không chia sẻ JWT/password camera)
