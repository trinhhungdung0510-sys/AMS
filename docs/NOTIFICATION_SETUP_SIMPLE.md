# AMS v1.7 — Cài đặt thông báo đơn giản

Hướng dẫn dành cho **người dùng cuối**. Không cần biết SMTP, Port, Token hay OA ID.

## Giao diện

### Gmail

1. Bật **☑ Bật Gmail**
2. Nhập **Email nhận cảnh báo**
3. Bấm **Kết nối Gmail**
4. Khi thành công: **✓ Đã kết nối**

AMS tự cấu hình máy chủ gửi mail — người dùng không nhập SMTP.

### Zalo

1. Bật **☑ Bật Zalo**
2. Bấm **Quét mã QR**
3. Mở Zalo trên điện thoại → quét mã → **Quan tâm** Official Account AMS
4. Khi thành công: **✓ Đã kết nối**

AMS tự lưu User ID và token — người dùng không nhập OA ID hay Access Token.

### Lưu cấu hình

Bấm **Lưu cấu hình** để lưu trạng thái bật/tắt Gmail và Zalo vào **Database** (PostgreSQL).

---

## Tự động gửi khi có vi phạm

Khi Compliance Engine tạo vi phạm **OPEN**, AMS tự động:

```
Dashboard → Zalo → Gmail
```

Không cần thao tác thủ công.

---

## Quản trị viên hệ thống (một lần khi triển khai)

Người dùng cuối **không** thấy các biến sau. Quản trị viên cấu hình trong `backend/.env`:

```env
# Gmail — tài khoản hệ thống gửi cảnh báo
SMTP_USER=ams-alerts@company.com
SMTP_PASSWORD=google-app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

# Zalo OA — Official Account của trang trại
ZALO_OA_ID=1234567890123456789
ZALO_OA_ACCESS_TOKEN=your-oa-access-token
# Tùy chọn: URL quan tâm OA tùy chỉnh
# ZALO_OA_FOLLOW_URL=https://zalo.me/your-oa
```

Sau khi cấu hình `.env`, khởi động lại backend. Người dùng chỉ cần kết nối qua UI.

---

## API (cho tích hợp / kiểm thử)

| Endpoint | Mô tả |
|----------|--------|
| `GET /api/notifications/settings` | Trạng thái đơn giản (connected flags) |
| `PUT /api/notifications/settings` | Lưu bật/tắt + email |
| `POST /api/notifications/connect/gmail` | Kết nối Gmail |
| `POST /api/notifications/connect/zalo/start` | Bắt đầu quét QR |
| `GET /api/notifications/connect/zalo/status/{session_id}` | Kiểm tra đã quét chưa |

---

## Kiểm tra thực tế

### Gmail

1. Quản trị viên cấu hình `SMTP_USER` + `SMTP_PASSWORD` trong `.env`
2. Người dùng: nhập email → **Kết nối Gmail** → thấy **✓ Đã kết nối**
3. Gọi thử (API): `POST /api/notifications/test` body `{"channel":"gmail"}` hoặc tạo vi phạm OPEN

### Zalo

1. Quản trị viên cấu hình `ZALO_OA_ID` + `ZALO_OA_ACCESS_TOKEN`
2. Người dùng: **Quét mã QR** → quan tâm OA trên điện thoại
3. UI hiển thị **✓ Đã kết nối** khi AMS phát hiện follower mới

### Build

```bash
cd backend && .venv/bin/python -m pytest -q
npm run build
```

---

## Xử lý lỗi thường gặp

| Thông báo | Nguyên nhân | Cách xử lý |
|-----------|-------------|------------|
| Hệ thống chưa sẵn sàng gửi Gmail | Thiếu SMTP trong `.env` | Liên hệ quản trị viên |
| Không kết nối được Gmail | App Password sai | Kiểm tra lại `.env` |
| Hệ thống chưa sẵn sàng gửi Zalo | Thiếu OA ID / Token | Liên hệ quản trị viên |
| Phiên quét mã QR hết hạn | Quá 10 phút chưa quét | Bấm **Quét mã QR** lại |

---

## Tài liệu liên quan

- Chi tiết kỹ thuật production: [`NOTIFICATION_PRODUCTION.md`](NOTIFICATION_PRODUCTION.md)
- Luồng tự động: [`AUTO_NOTIFICATION_WORKFLOW.md`](AUTO_NOTIFICATION_WORKFLOW.md)
