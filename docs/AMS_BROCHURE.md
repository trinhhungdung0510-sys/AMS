# AMS — Animal Management & Biosecurity System

**Giám sát an toàn sinh học thông minh cho trang trại chăn nuôi quy mô**

---

## Vấn đề thực tế

Trang trại hiện đại phải tuân thủ quy trình ATSH nghiêm ngặt: đồng phục, vùng cấm, sát trùng, kiểm soát xe và động vật lạ. Giám sát thủ công không đủ tốc độ, không có bằng chứng, khó truy vết khi có sự cố.

AMS giúp chuyển từ **“phát hiện muộn”** sang **“cảnh báo realtime + bằng chứng có hệ thống”**.

---

## AMS là gì?

**AMS (Animal Management System)** là nền tảng phần mềm giám sát tuân thủ an toàn sinh học trên camera IP, tích hợp:

- Phát hiện vi phạm quy trình (đồng phục, xâm nhập vùng, động vật, phương tiện)
- Dashboard realtime qua WebSocket
- Lưu trữ evidence (snapshot) theo sự kiện
- Quản lý đa trại (multi-farm) và phân quyền RBAC
- Triển khai trong 1 ngày với Setup Wizard

---

## Giá trị cốt lõi

| Lợi ích | Mô tả |
|---------|--------|
| **Giảm rủi ro dịch bệnh** | Phát hiện vi phạm ATSH sớm, có bằng chứng hình ảnh |
| **Truy vết nhanh** | Event catalog phân loại, mức độ nghiêm trọng, khuyến nghị xử lý |
| **Vận hành tập trung** | Một dashboard cho nhiều trại, nhiều camera |
| **Triển khai nhanh** | Setup Wizard 5 bước, health check, export/import cấu hình |
| **Demo không cần camera** | Demo Mode cho sales, training, pilot nội bộ |

---

## Tính năng nổi bật

### Giám sát tuân thủ (Compliance)

- Sai đồng phục bảo hộ
- Xâm nhập vùng cấm
- Động vật / phương tiện xâm nhập trái phép
- Vi phạm quy trình ATSH (nhà tắm, rửa tay, sát trùng ủng)

### Vận hành & triển khai

- **Setup Wizard** — Farm → Camera → Zone → Uniform → System Check
- **System Status** — camera online/offline, RTSP, CPU, RAM, storage
- **Diagnostics** — test zone, test rule, export/import config
- **Evidence Browser** — duyệt snapshot theo farm, camera, ngày, rule

### Quản trị doanh nghiệp

- Multi-farm tenancy
- RBAC: SUPER_ADMIN, FARM_ADMIN, VIEWER
- Audit log, backup/restore, retention policy
- Báo cáo compliance KPI (score, top violations)

---

## Ai nên dùng AMS?

- **Chuỗi trang trại heo/gia cầm** cần chuẩn hóa ATSH giữa các site
- **Trại quy mô lớn** có nhiều cổng, nhà tắm, hàng rào cần giám sát 24/7
- **Đội vận hành / QA** cần dashboard và báo cáo tuân thủ
- **Đối tác tích hợp** triển khai giải pháp camera + phần mềm cho khách hàng

---

## Demo trong 15 phút

```bash
# Bật demo — không cần camera thật
DEMO_MODE=true

# Khởi động backend + frontend
# Đăng nhập → Dashboard hiển thị event realtime
```

Farm demo mặc định: **Mind Farm Demo** — Nhà tắm, Cổng trại, Hàng rào.

---

## Kiến trúc tin cậy

```
Camera RTSP → Backend (FastAPI) → Event Pipeline → WebSocket → Dashboard
                    ↓
              PostgreSQL + Evidence Storage
```

- API REST + WebSocket `/ws/events`
- Health API: `GET /api/health`
- Deployment check: `node scripts/deploymentCheck.js`

---

## Bước tiếp theo

| Tài liệu | Mục đích |
|----------|----------|
| [AMS_SOLUTION_OVERVIEW.md](./AMS_SOLUTION_OVERVIEW.md) | Chi tiết giải pháp kỹ thuật |
| [AMS_DEPLOYMENT_GUIDE.md](./AMS_DEPLOYMENT_GUIDE.md) | Hướng dẫn triển khai |
| [AMS_PILOT_PLAN.md](./AMS_PILOT_PLAN.md) | Kế hoạch pilot tại trại |
| [AMS_PRICING_MODEL.md](./AMS_PRICING_MODEL.md) | Mô hình giá tham khảo |

---

**AMS v2.0** — Product-ready · Multi-farm · Deployment Kit · Demo Mode

*Liên hệ đội triển khai để demo onsite hoặc pilot 30–60 ngày.*
