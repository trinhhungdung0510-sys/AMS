# AMS v2.0 — Camera Setup

Hướng dẫn thêm camera và kiểm tra zone trước khi chạy production.

## Prerequisites

- Camera hỗ trợ RTSP (H.264 khuyến nghị)
- FFmpeg cài trên server AMS
- Network: server AMS ↔ camera cùng VLAN hoặc route được

## Step 1 — Add Camera (Setup Wizard)

Route: `/setup` → Bước 2

| Field | Example |
|-------|---------|
| ID | CAM-GATE-01 |
| Name | Cổng vào trại |
| Farm ID | FARM-001 |
| IP | 192.168.1.100 |
| Port | 554 |
| RTSP path | `/Streaming/Channels/101` |

AMS build RTSP URL:

```
rtsp://{username}:{password}@{ip}:{port}{path}
```

Lưu credentials trong camera record — không log ra client.

## Step 2 — Verify Reachability

**System Status** (`/system-status`):

- Camera Online / Offline counts
- RTSP / FFmpeg status

**Diagnostics** (`/diagnostics`):

- `cameraReachability[]` — ping RTSP probe per camera

**API**:

```bash
curl http://localhost:8000/api/health | jq '.camera'
```

## Step 3 — Define Zone

### Option A — Setup Wizard (Bước 3)

Tạo zone polygon mặc định trên camera. Dùng cho triển khai nhanh.

### Option B — Zone Designer

Route: `/zone-designer` hoặc camera detail — vẽ polygon chính xác trên frame.

Coordinates lưu dạng normalized (0–1) theo kích thước frame.

## Step 4 — Zone Test Mode

Trước go-live, test từng zone:

1. Mở **Diagnostics** (`/diagnostics`)
2. Nhập Zone ID
3. Click **Test Zone**

Hiển thị:

- Zone name
- Overlay coordinates
- Camera ID / source type

API:

```bash
GET /api/deployment/zones/{zone_id}/test
```

Response mẫu:

```json
{
  "zoneId": "ZONE-001",
  "zoneName": "Cổng vào",
  "cameraId": "CAM-GATE-01",
  "coordinates": [[0.1, 0.2], [0.5, 0.2], [0.5, 0.8], [0.1, 0.8]],
  "overlay": { "type": "polygon", "points": "..." }
}
```

## Step 5 — Uniform (Compliance)

Setup Wizard Bước 4 — tạo uniform template gắn với farm/zone.

Test rule:

```bash
POST /api/deployment/rules/test
{ "ruleType": "UNIFORM_VIOLATION", "trackId": 101, "score": 0.72 }
```

## Camera Brands — RTSP Paths

| Brand | Typical path |
|-------|----------------|
| Hikvision | `/Streaming/Channels/101` |
| Dahua | `/cam/realmonitor?channel=1&subtype=0` |
| Axis | `/axis-media/media.amp` |
| Reolink | `/h264Preview_01_main` |

Dùng VLC hoặc `ffprobe` để xác nhận stream:

```bash
ffprobe -rtsp_transport tcp "rtsp://user:pass@192.168.1.100:554/..."
```

## Performance Tips

- Sub-stream (lower resolution) cho detection nếu camera hỗ trợ
- Giới hạn số camera per GPU theo capacity server
- Monitor CPU/RAM trên **System Status**

## Export Camera Config

Backup camera settings:

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/deployment/export/camera.json -o camera.json
```

Restore qua Import Config trên Diagnostics page.

## Related

- [INSTALL.md](./INSTALL.md)
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) — camera offline, ffmpeg
