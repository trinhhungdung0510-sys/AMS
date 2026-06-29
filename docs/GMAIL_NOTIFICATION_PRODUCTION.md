# AMS v1.7 — Gmail Notification (Production)

Tài liệu triển khai gửi Email cảnh báo vi phạm ATSH qua **Gmail SMTP thật**.

## Kiến trúc

```
AI Detection → Rule Engine → Compliance Engine
        → Violation OPEN (event.created)
        → Violation Notification Subscriber
        → Gmail Notification Service
        → SMTP (backend/.env)
        → Email quản lý
```

**Không thay đổi:** Rule Engine, Compliance Engine, Workflow, AI Detection, Event Pipeline.

**Bổ sung:** `Gmail Notification Service` + API `/api/notification/*`

## Cấu hình SMTP (chỉ backend/.env)

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-sender@gmail.com
SMTP_PASSWORD=your-google-app-password
```

Frontend **không** gửi/nhận các giá trị này.

Email nhận cảnh báo (`gmail_recipient`) lưu trong **Database** (`system_settings`).

## API

| Method | Path | Mô tả |
|--------|------|--------|
| POST | `/api/notification/gmail/connect` | Kiểm tra SMTP + gửi email xác nhận |
| POST | `/api/notification/gmail/test` | Gửi email thử vi phạm mẫu |
| POST | `/api/notification/send` | Gửi email vi phạm (payload event) |

### POST `/api/notification/gmail/connect`

Body:

```json
{ "gmail_recipient": "manager@company.com" }
```

Response thành công:

```json
{ "connected": true, "gmail_recipient": "manager@company.com" }
```

Lỗi (400): Authentication failed, thiếu `.env`, không kết nối SMTP…

### POST `/api/notification/gmail/test`

Gửi email thử tới `gmail_recipient` đã lưu. Ghi Notification Log.

### POST `/api/notification/send`

Body (tối thiểu):

```json
{
  "event_id": "EVT-ABC123",
  "farm_id": "FARM-001",
  "camera_name": "Camera 1",
  "zone_name": "Khu A",
  "rule_name": "Không sát trùng tay",
  "severity": "HIGH",
  "description": "Mô tả vi phạm"
}
```

Luồng tự động từ Compliance **không** gọi HTTP — dùng cùng service nội bộ qua Event Bus subscriber.

## Luồng gửi tự động

1. Compliance Engine tạo Event `OPEN`
2. `EVENT_CREATED` → `dispatch_violation_notifications`
3. Dashboard → Zalo → **Gmail** (theo thứ tự)
4. Gmail: `send_gmail_message()` qua SMTP `.env`

## Nội dung Email

**Tiêu đề:** `🚨 CẢNH BÁO VI PHẠM AN TOÀN SINH HỌC`

**HTML gồm:** Trang trại, Camera, Khu vực, Thời gian, Quy tắc ATSH, Mức độ, Mô tả

- Snapshot: đính kèm file local hoặc nhúng ảnh (cid)
- Video: link trong email
- Nút **Mở AMS** → chi tiết vi phạm

## Chống gửi lặp

- `notification_dispatches.event_id` (PK)
- `notification_deliveries` UNIQUE (`event_id`, `channel`)

Một Violation ID → Gmail gửi **1 lần** (kể cả refresh/restart).

## Notification Log

Bảng `notification_deliveries`:

| Cột | Ý nghĩa |
|-----|---------|
| `event_id` | Violation ID |
| `sent_at` | Thời gian gửi |
| `recipient` | Email người nhận |
| `channel` | `gmail` |
| `status` | `success` / `failed` |
| `error_message` | Lỗi SMTP (nếu có) |

Migration: `0036_notification_recipient` (cột `recipient`)

## Frontend

**Cài đặt → Thông báo vi phạm ATSH**

- ☑ Bật Gmail
- Email nhận cảnh báo
- **[Kết nối Gmail]** → `POST /api/notification/gmail/connect`
- **[Lưu]**

Ẩn: SMTP Host, Port, User, Password.

## Kiểm thử

```bash
cd backend
.venv/bin/alembic upgrade head
.venv/bin/python -m pytest tests/test_gmail_notification_service.py tests/test_violation_notification_service.py -q
cd .. && npm run build
```

## File chính

| File | Vai trò |
|------|---------|
| `backend/app/services/gmail_notification_service.py` | SMTP, HTML email, connect, send |
| `backend/app/api/notification.py` | API production |
| `backend/app/services/violation_notification_service.py` | Auto-dispatch + dedup |
| `src/services/notificationSettingsService.js` | Client API |
| `src/pages/SettingsPage.jsx` | UI đơn giản |
