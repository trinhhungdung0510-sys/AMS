# AMS Pilot Acceptance Checklist

Checklist nghiệm thu pilot AMS tại trang trại. Đánh dấu **PASS** hoặc **FAIL** cho từng hạng mục sau khi kiểm tra thực tế onsite.

**Trang trại:** ___________________________  
**Ngày nghiệm thu:** _____________________  
**Người kiểm tra:** ______________________  
**Phiên bản AMS:** _______________________

---

## Camera

| # | Hạng mục | Cách kiểm tra | PASS | FAIL | Ghi chú |
|---|----------|---------------|:----:|:----:|---------|
| 1 | Camera online | Camera hiển thị trạng thái online trên Dashboard / System Status | ☐ | ☐ | |
| 2 | RTSP hoạt động | Stream preview hoặc detector nhận frame từ URL RTSP | ☐ | ☐ | |
| 3 | Snapshot hoạt động | Chụp snapshot thủ công hoặc tự động khi có event | ☐ | ☐ | |

---

## Zone

| # | Hạng mục | Cách kiểm tra | PASS | FAIL | Ghi chú |
|---|----------|---------------|:----:|:----:|---------|
| 1 | Zone vẽ đúng | Polygon khớp vùng thực tế trên overlay camera | ☐ | ☐ | |
| 2 | Zone lưu đúng | Lưu zone → API trả thành công, không mất điểm | ☐ | ☐ | |
| 3 | Zone load lại đúng | Refresh trang / mở lại Zone Designer → polygon giữ nguyên | ☐ | ☐ | |

---

## Compliance

| # | Hạng mục | Cách kiểm tra | PASS | FAIL | Ghi chú |
|---|----------|---------------|:----:|:----:|---------|
| 1 | Uniform Violation | Phát hiện sai đồng phục trong vùng có gán uniform | ☐ | ☐ | |
| 2 | Zone Intrusion | Phát hiện xâm nhập / vào vùng cấm | ☐ | ☐ | |
| 3 | Animal Intrusion | Phát hiện động vật trong vùng cấm (nếu bật rule) | ☐ | ☐ | |

---

## Workflow

| # | Hạng mục | Cách kiểm tra | PASS | FAIL | Ghi chú |
|---|----------|---------------|:----:|:----:|---------|
| 1 | Process Completed | Workflow hoàn tất đúng bước khi không vi phạm | ☐ | ☐ | |
| 2 | Process Violation | Workflow tạo / xử lý violation đúng trạng thái | ☐ | ☐ | |

---

## Dashboard

| # | Hạng mục | Cách kiểm tra | PASS | FAIL | Ghi chú |
|---|----------|---------------|:----:|:----:|---------|
| 1 | Realtime | Event mới xuất hiện trên dashboard / WS feed (< 30s) | ☐ | ☐ | |
| 2 | Filter | Lọc theo camera, zone, loại vi phạm, thời gian hoạt động | ☐ | ☐ | |
| 3 | Evidence | Xem snapshot / evidence gắn với event vi phạm | ☐ | ☐ | |

---

## Reporting

| # | Hạng mục | Cách kiểm tra | PASS | FAIL | Ghi chú |
|---|----------|---------------|:----:|:----:|---------|
| 1 | Daily Summary | Báo cáo tổng hợp ngày hiển thị đúng số liệu | ☐ | ☐ | |
| 2 | Top Violations | Danh sách vi phạm hàng đầu theo loại / zone | ☐ | ☐ | |

---

## System

| # | Hạng mục | Cách kiểm tra | PASS | FAIL | Ghi chú |
|---|----------|---------------|:----:|:----:|---------|
| 1 | Backup | Tạo backup cấu hình / dữ liệu thành công | ☐ | ☐ | |
| 2 | Restore | Khôi phục từ backup, hệ thống hoạt động sau restore | ☐ | ☐ | |
| 3 | Health Check | `GET /api/health` và System Status = ok / degraded chấp nhận được | ☐ | ☐ | |

---

## Tổng kết

| Nhóm | PASS | FAIL | Tổng |
|------|------|------|------|
| Camera | | | 3 |
| Zone | | | 3 |
| Compliance | | | 3 |
| Workflow | | | 2 |
| Dashboard | | | 3 |
| Reporting | | | 2 |
| System | | | 3 |
| **Tổng cộng** | | | **19** |

**Tiêu chí nghiệm thu pilot:** ≥ 90% hạng mục PASS (≥ 17/19), không có FAIL ở nhóm **Camera**, **Compliance**, **System → Health Check**.

| Kết quả | ☐ **PASS** — Sẵn sàng mở rộng / kết thúc pilot thành công |
|---------|-------------------------------------------------------------|
|         | ☐ **FAIL** — Cần khắc phục trước khi nghiệm thu |

**Chữ ký Ban ATSH:** _________________________  **Ngày:** ___________

**Chữ ký AMS / triển khai:** __________________  **Ngày:** ___________

---

*Tham chiếu: [AMS_PILOT_PLAN.md](./AMS_PILOT_PLAN.md)*
