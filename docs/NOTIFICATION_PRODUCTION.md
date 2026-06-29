# AMS v1.7 — Notification Service (Production)

Tài liệu triển khai **Notification Service thực tế** cho hệ thống AMS. Không sử dụng mock, fake API, hay phản hồi demo.

## Tổng quan

Khi Compliance Engine tạo vi phạm **OPEN**, Notification Service tự động gửi theo thứ tự:

1. **Dashboard** (WebSocket `notification.created` + `event.created`)
2. **Zalo OA** (Zalo Open API)
3. **Gmail** (SMTP thật)

Mỗi `event_id` chỉ được gửi **một lần** (bảng `notification_dispatches` + `notification_deliveries`).

---

## Lưu cấu hình (Database)

Cấu hình lưu trong bảng `system_settings`, key `violation_notification_settings`.

| Trường | Mô tả |
|--------|--------|
| `gmail_enabled` | Bật/tắt Gmail |
| `gmail_recipient` | Email nhận cảnh báo |
| `gmail_from` | Email hiển thị người gửi (From) |
| `smtp_host` | Máy chủ SMTP (vd: `smtp.gmail.com`) |
| `smtp_port` | Cổng SMTP (mặc định `587`) |
| `smtp_user` | Tài khoản SMTP |
| `smtp_password` | Mật khẩu / App Password |
| `zalo_enabled` | Bật/tắt Zalo |
| `zalo_oa_id` | OA Zalo ID |
| `zalo_recipient_id` | User ID người nhận trên Zalo |
| `zalo_access_token` | OA Access Token |
| `ams_app_url` | URL mở AMS trong thông báo |

**API:**

- `GET /api/notifications/settings` — đọc cấu hình (mật khẩu/token được ẩn, có cờ `*_set`)
- `PUT /api/notifications/settings` — lưu cấu hình (yêu cầu `settings.write`)

Khởi động lại backend **vẫn giữ** cấu hình vì lưu PostgreSQL, không dùng LocalStorage.

---

## Biến môi trường (tùy chọn)

Có thể cấu hình SMTP/Zalo qua `backend/.env` làm fallback nếu UI chưa điền:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=your-app-password
ZALO_OA_ACCESS_TOKEN=your-zalo-oa-token
```

Ưu tiên: **cấu hình trong UI** → sau đó mới fallback `.env`.

---

## Gmail (SMTP thật)

### Cấu hình Gmail

1. Bật xác minh 2 bước trên Google Account.
2. Tạo **App Password**: Google Account → Security → App passwords.
3. Trong AMS **Cài đặt → Thông báo vi phạm ATSH**:

| Trường | Giá trị mẫu |
|--------|-------------|
| SMTP Host | `smtp.gmail.com` |
| SMTP Port | `587` |
| SMTP User | `your@gmail.com` |
| SMTP Password | App Password 16 ký tự |
| Email nhận | địa chỉ nhận cảnh báo |
| Email gửi (From) | thường trùng SMTP User |

4. **Lưu cấu hình** → **Thử Gmail**.

### Hành vi

- Kết nối SMTP thật qua `smtplib`.
- Thành công: trả về `status: success`, ghi nhật ký `notification_deliveries`.
- Thất bại: trả về lỗi chi tiết (SMTP auth, timeout, v.v.).

---

## Zalo OA (API thật)

### Cấu hình

1. Đăng ký OA tại [Zalo Developers](https://developers.zalo.me/).
2. Lấy **OA ID** và **Access Token** (OA → Công cụ → API).
3. Lấy **User ID** người nhận (user đã quan tâm OA).
4. Điền vào AMS Settings → **Lưu cấu hình** → **Thử Zalo**.

### API sử dụng

```
POST https://openapi.zalo.me/v3.0/oa/message/cs
Header: access_token
Body: { recipient: { user_id }, message: { text } }
```

Phản hồi lỗi Zalo (`error`, `message`) được hiển thị trực tiếp trên UI.

---

## Dashboard (Event Pipeline)

### Nút "Thử Dashboard"

1. Tạo vi phạm **ảo** (`metadata.ephemeral = true`), **không ghi DB**.
2. Publish `event.created` qua Event Bus → EventStreamService → WebSocket `/ws/events`.
3. Gửi `notification.created` (toast cảnh báo ATSH).
4. Sau **5 giây** publish `event.removed` → client xóa khỏi feed.

Luồng giống vi phạm thật trên dashboard realtime feed.

### Vi phạm thật (Compliance Engine)

```
Compliance Engine → EVENT_CREATED (DB)
       ↓
Violation Notification Subscriber
       ↓
Dashboard → Zalo → Gmail (ghi nhật ký, chống trùng event_id)
       ↓
WebSocket → Frontend toast + event feed
```

---

## Chống gửi lặp

| Cơ chế | Bảng / Ràng buộc |
|--------|------------------|
| Claim dispatch | `notification_dispatches` PK = `event_id` |
| Mỗi kênh 1 lần | `notification_deliveries` UNIQUE (`event_id`, `channel`) |

Refresh trang, reload, restart backend **không gửi lại** cùng vi phạm.

---

## Nhật ký gửi

Bảng `notification_deliveries`:

| Cột | Ý nghĩa |
|-----|---------|
| `sent_at` | Thời gian gửi (ISO UTC) |
| `channel` | `dashboard` / `gmail` / `zalo` |
| `status` | `success` / `failed` / `skipped` |
| `error_message` | Nội dung lỗi (nếu có) |
| `subject` | Tiêu đề thông báo |

**API:** `GET /api/notifications/deliveries?limit=50`

UI Settings hiển thị 10 bản ghi gần nhất sau khi thử Gmail/Zalo.

---

## Kiểm thử thực tế

### Checklist

- [ ] **Gmail:** Cấu hình SMTP → Thử Gmail → nhận email thật
- [ ] **Zalo:** Cấu hình OA ID + Token + User ID → Thử Zalo → nhận tin nhắn Zalo
- [ ] **Dashboard:** Thử Dashboard → thấy vi phạm trên feed WS + toast → tự biến mất sau ~5s
- [ ] **Lưu cấu hình:** Lưu → restart backend → cấu hình còn nguyên
- [ ] **Tự động:** Tạo vi phạm OPEN từ Compliance → nhận cả 3 kênh (nếu bật)
- [ ] **Chống lặp:** Cùng `event_id` không gửi lại sau refresh

### Lệnh kiểm tra API

```bash
TOKEN=$(curl -sf -X POST http://127.0.0.1:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@ams.local","password":"admin123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl -sf -X PUT -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"smtp_host":"smtp.gmail.com","smtp_port":587,"smtp_user":"you@gmail.com","smtp_password":"APP_PASSWORD","gmail_recipient":"you@gmail.com"}' \
  http://127.0.0.1:8000/api/notifications/settings

curl -sf -X POST -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"channel":"gmail"}' \
  http://127.0.0.1:8000/api/notifications/test

curl -sf -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/notifications/deliveries
```

### Migration

```bash
cd backend && .venv/bin/alembic upgrade head
```

Revision: `0035_violation_notification`

---

## Quy trình triển khai Production

1. **Database:** Chạy migration `0035`, backup trước khi deploy.
2. **Secrets:** Cấu hình SMTP và Zalo qua UI hoặc biến môi trường trên server (không commit `.env`).
3. **Network:** Server backend cần outbound HTTPS (Zalo API) và SMTP (port 587/465).
4. **WebSocket:** Reverse proxy (nginx) phải hỗ trợ upgrade cho `/ws/events`.
5. **Kiểm tra:** Chạy checklist trên môi trường staging trước production.
6. **Giám sát:** Theo dõi `GET /api/notifications/deliveries` và log backend `[Notification]`.

---

## File liên quan

| Thành phần | Path |
|------------|------|
| Service | `backend/app/services/violation_notification_service.py` |
| API | `backend/app/api/notifications.py` |
| Event → WS | `backend/app/services/event_stream_service.py` |
| UI Settings | `src/pages/SettingsPage.jsx` |
| WS Client | `src/context/EventStore.jsx` |
| Toast | `src/providers/NotificationProvider.jsx` |
