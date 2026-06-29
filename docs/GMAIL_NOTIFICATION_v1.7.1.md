# Gmail Notification Production — AMS v1.7.1

Tài liệu mô tả hệ thống cảnh báo Gmail production cho vi phạm ATSH (OPEN).

## Phạm vi Gmail (v1.7)

Gmail **chỉ** gửi cảnh báo tức thời:

| Loại | Kích hoạt |
|------|-----------|
| Vi phạm ATSH OPEN | Compliance Engine → `event.created` |
| Email thử | Settings → «Gửi Email thử» |
| Cảnh báo hệ thống | Camera OFFLINE, AI Runtime dừng, DB unavailable, Gmail lỗi liên tiếp |

**Không triển khai:** báo cáo ngày/tuần/tháng, digest, tổng hợp thống kê qua email.

### Email vi phạm (v1.7.1)

**Tiêu đề:** `🚨 CẢNH BÁO VI PHẠM AN TOÀN SINH HỌC` — không chứa mã vi phạm.

**Nội dung hiển thị:**

Thời gian · Camera · Khu vực · Quy tắc ATSH vi phạm · Mức độ · Mô tả · Snapshot (nếu có) · **Mở AMS**

**Không hiển thị:** Mã vi phạm (không trong tiêu đề, không trong nội dung).

### Phạm vi gửi vi phạm

Mọi vi phạm do **Compliance Engine** xác nhận với trạng thái **OPEN** đều tự động gửi Email — **không lọc theo rule**, không cấu hình từng loại.

Bao gồm toàn bộ quy tắc ATSH: sai đồng phục, không sát trùng tay/ủng, xe chưa sát trùng, vào vùng cấm, tiếp xúc xe cám/người lạ, động vật xâm nhập, v.v.

Điều kiện kỹ thuật: `is_compliance_open_violation()` — `category=compliance_violation` hoặc `metadata.source=compliance_engine` + status OPEN.

### Cảnh báo hệ thống

`system_alert_notification_service.py` — subscriber EventBus, cooldown 30 phút/loại, gửi background.

---

## Kiến trúc

```
Compliance Engine (OPEN violation)
        │
        ▼
EventBus: event.created
        │
        ▼
ViolationNotificationService.handle_event_created_for_notifications
        │
        ▼
dispatch_violation_notifications
   ├── Dashboard (sync, WebSocket toast)
   ├── Zalo OA (sync, HTTP)
   └── Gmail SMTP (background thread, timeout 10s)
```

**Phạm vi thay đổi v1.7.1:** chỉ Notification Service. Không thay đổi AI Detection, Rule Engine, Compliance Engine, Workflow Engine, Event Pipeline.

### Thành phần chính

| Thành phần | Vai trò |
|------------|---------|
| `violation_notification_service.py` | Orchestrator: dedup, dashboard/zalo sync, Gmail async |
| `gmail_notification_service.py` | SMTP Gmail, HTML email, connect/test |
| `notification_dispatches` | Một bản ghi / violation — chống gửi trùng toàn pipeline |
| `notification_deliveries` | Nhật ký từng kênh (gmail/zalo/dashboard) |
| `POST /api/notification/gmail/*` | Kết nối và gửi thử |
| Settings UI | Trạng thái Gmail, gửi thử, lỗi thật |

### Cấu hình SMTP

Chỉ đọc từ `backend/.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=app-password-16-chars
```

Email nhận cảnh báo lưu DB (`system_settings.violation_notification_settings.gmail_recipient`).

---

## Luồng gửi tự động

1. Compliance Engine tạo violation **OPEN** → publish `event.created`.
2. Subscriber kiểm tra:
   - Không phải event ephemeral/test
   - Status OPEN
   - Compliance Engine (`is_compliance_open_violation`) — mọi rule, không phân loại
3. **Dedup:** `notification_dispatches.event_id` (PK) — refresh/restart không gửi lại.
4. Per-channel dedup: `notification_deliveries (event_id, channel)` unique.
5. Dashboard + Zalo gửi đồng bộ (nhanh).
6. Gmail chạy **background thread** — không block Event Pipeline / Dashboard.
7. SMTP timeout **10 giây** — không treo backend.
8. Lỗi Gmail → WebSocket `notification.gmail_failed` + banner Dashboard.

---

## HTML Email

- **Tiêu đề:** `🚨 CẢNH BÁO VI PHẠM AN TOÀN SINH HỌC`
- **Header:** Logo AMS, Tín Nghĩa AMS, gradient xanh lá (#15803d) / cam (#ea580c)
- **Nội dung:** Thời gian, Camera, Khu vực, Quy tắc ATSH vi phạm, Mức độ, Mô tả
- **Mức độ:** 🟢 Thấp · 🟡 Trung bình · 🔴 Cao
- **Snapshot:** embed inline (`cid:violation-snapshot`) nếu có file/URL
- **CTA:** nút «Mở AMS» → URL ứng dụng AMS (`ams_app_url`)
- **Footer:** «Tự động gửi bởi Tín Nghĩa AMS»
- **Không có:** Mã vi phạm trong email

---

## Notification Log

Bảng `notification_deliveries`:

| Cột | Mô tả |
|-----|--------|
| `event_id` | Violation ID |
| `channel` | `gmail` / `zalo` / `dashboard` |
| `recipient` | Email nhận (Gmail) |
| `sent_at` | Thời gian gửi (ISO UTC) |
| `smtp_latency_ms` | Thời gian phản hồi SMTP (ms) |
| `status` | `success` / `failed` / `skipped` |
| `error_message` | Lỗi thật nếu có |

API: `GET /api/notifications/deliveries`

Settings API bổ sung (từ delivery Gmail mới nhất):

- `gmail_last_sent_at`
- `gmail_last_status`
- `gmail_last_error`

---

## Giao diện

**Settings → Thông báo vi phạm ATSH**

- ✓ Đã kết nối Gmail
- Email nhận
- Lần gửi cuối
- Trạng thái (Thành công / Gửi thất bại)
- Nút **Gửi Email thử** → `POST /api/notification/gmail/test`
- Lỗi hiển thị nguyên nhân thật (Authentication failed, SMTP timeout, Recipient rejected, …)

**Dashboard:** banner đỏ «Gửi Email thất bại» khi Gmail lỗi (WS hoặc trạng thái cuối).

---

## Kiểm thử

### Backend

```bash
cd backend
alembic upgrade head
pytest tests/test_gmail_notification_service.py tests/test_notification_production.py -q
pytest -q
```

### Frontend

```bash
npm run build
npm test -- --run
```

### Checklist thủ công (production)

- [ ] Cấu hình `SMTP_USER` + App Password trong `.env`
- [ ] Settings → Kết nối Gmail (email xác nhận)
- [ ] Gửi Email thử → nhận email HTML đúng mẫu
- [ ] Tạo violation OPEN → 1 email duy nhất / violation ID
- [ ] Restart backend → không gửi lại email cũ
- [ ] Sai password → UI + Dashboard hiển thị lỗi Authentication failed
- [ ] `notification_deliveries` có bản ghi + `smtp_latency_ms`

---

## Các lỗi đã xử lý

| Lỗi | Xử lý |
|-----|--------|
| Gửi trùng khi refresh/restart | PK `notification_dispatches` + unique `(event_id, channel)` |
| SMTP treo backend | Timeout 10s + Gmail trong background thread |
| Block Event Pipeline | Dashboard/Zalo sync; Gmail detached |
| Lỗi SMTP che giấu | `_normalize_smtp_error`: Authentication failed, timeout, recipient rejected |
| Admin không biết Gmail fail | WS `notification.gmail_failed` + banner + Settings status |
| Snapshot không hiện trong email | Inline CID từ file local hoặc HTTP download |
| Credential lộ qua UI | SMTP chỉ từ `.env`; API mask secrets |

---

## API tham chiếu

| Method | Path | Mô tả |
|--------|------|--------|
| POST | `/api/notification/gmail/connect` | Verify SMTP + email xác nhận |
| POST | `/api/notification/gmail/test` | Email thử vi phạm mẫu |
| POST | `/api/notification/send` | Gửi thủ công (admin) |
| GET | `/api/notifications/settings` | Cấu hình + trạng thái Gmail |
| GET | `/api/notifications/deliveries` | Nhật ký gửi |

---

*AMS v1.7.1 — Production. Không mock SMTP. Email gửi thật qua Gmail.*
