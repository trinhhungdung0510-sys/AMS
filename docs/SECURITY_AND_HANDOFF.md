# AMS v1.7 — Bảo mật tài liệu & handoff

Tài liệu này giúp tiếp tục công việc ngày hôm sau mà **không lộ secret**.

## File KHÔNG được commit

| File / thư mục | Lý do |
|----------------|--------|
| `backend/.env` | SMTP password, Zalo token, JWT secret |
| `.env.local` | Biến môi trường local |
| `backups/*.sql` | Dump database có thể chứa dữ liệu thật |
| `backend/test_venv/` | Virtualenv local |

Đã có trong `.gitignore`. **Không** `git add` các file trên.

Chỉ commit mẫu: `backend/.env.example` (placeholder, không có secret thật).

## Tài liệu an toàn (đã kiểm tra)

Các file docs chỉ dùng **placeholder** (`your@gmail.com`, `APP_PASSWORD`, `your-zalo-oa-token`):

- `docs/NOTIFICATION_SETUP_SIMPLE.md` — hướng dẫn người dùng
- `docs/NOTIFICATION_PRODUCTION.md` — triển khai production
- `docs/AUTO_NOTIFICATION_WORKFLOW.md` — luồng tự động

Mật khẩu dev mặc định `admin123` / `ams_password` chỉ xuất hiện trong hướng dẫn cài đặt local (không dùng production).

## Cấu hình thông báo (ngày mai)

1. Mở `backend/.env` (file local, không commit)
2. Điền:

```env
SMTP_USER=...
SMTP_PASSWORD=...          # Google App Password
ZALO_OA_ID=...
ZALO_OA_ACCESS_TOKEN=...
```

3. Restart backend
4. UI: **Cài đặt → Thông báo vi phạm ATSH → Kết nối Gmail / Quét mã QR**

Chi tiết: [`NOTIFICATION_SETUP_SIMPLE.md`](NOTIFICATION_SETUP_SIMPLE.md)

## Trạng thái code (chưa commit)

Notification Service v1.7 nằm trên working tree local (`git status` có nhiều file modified/untracked). Trước khi push:

- [ ] Không stage `backend/.env`
- [ ] Không stage `backups/*.sql`
- [ ] Review diff docs trước khi commit

## Lưu ý `backups/ams_v3_0.sql`

File này **đã được track** trong git từ trước (trước khi thêm `backups/` vào `.gitignore`). Nếu dump chứa dữ liệu nhạy cảm, cân nhắc xóa khỏi lịch sử git hoặc thay bằng dump đã anonymize — liên hệ người quản lý repo trước khi force-push.

## Tiếp tục ngày mai

| Việc | Tài liệu |
|------|----------|
| Cấu hình `.env` | `NOTIFICATION_SETUP_SIMPLE.md` |
| Kiểm tra Gmail/Zalo thật | `NOTIFICATION_PRODUCTION.md` |
| Luồng tự động vi phạm | `AUTO_NOTIFICATION_WORKFLOW.md` |
| UI đơn giản | `NOTIFICATION_SETUP_SIMPLE.md` |

Migration nếu chưa chạy:

```bash
cd backend && .venv/bin/alembic upgrade head
```
