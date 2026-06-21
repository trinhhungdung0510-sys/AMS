# AMS — Pilot Plan

Kế hoạch triển khai **pilot AMS** tại 1 trang trại thực tế, thời gian khuyến nghị **30–60 ngày**, trước khi mở rộng multi-site.

---

## 1. Mục tiêu pilot

| Mục tiêu | Chỉ số thành công |
|----------|-------------------|
| Xác nhận giá trị ATSH | Phát hiện ≥80% vi phạm có kiểm chứng thủ công |
| Ổn định vận hành | Uptime backend ≥99% trong giờ cao điểm |
| Khả năng triển khai | Setup Wizard hoàn tất ≤1 ngày onsite |
| Chấp nhận người dùng | ≥3 FARM_ADMIN/VIEWER dùng dashboard hàng ngày |
| Sẵn sàng scale | Export config + báo cáo compliance 30 ngày |

---

## 2. Phạm vi pilot

### Trong phạm vi (In scope)

- 1 farm (1 site vật lý)
- 3–9 camera IP tại các điểm then chốt:
  - Nhà tắm / khu sát trùng người
  - Cổng trại / cổng xe
  - Hàng rào / biên vùng cấm
- Cấu hình zone polygon trên từng camera
- Uniform template cho vùng sản xuất
- Dashboard realtime + compliance KPI
- Evidence browser (snapshot vi phạm)
- Training vận hành (2 buổi)

### Ngoài phạm vi (Out of scope)

- Tích hợp ERP / MES
- Custom AI model training onsite
- Mobile app native
- Multi-farm central (có thể demo, không go-live pilot)
- SLA 24/7 enterprise (phase sau)

---

## 3. Timeline đề xuất (8 tuần)

### Tuần 0 — Pre-pilot (1 tuần)

| Ngày | Hoạt động | Deliverable |
|------|-----------|-------------|
| D-7 | Kickoff với Ban ATSH + IT trại | Biên bản phạm vi, danh sách camera |
| D-5 | Khảo sát mạng, VLAN camera | Sơ đồ IP, port RTSP |
| D-3 | Cài server AMS (staging) | Health check pass |
| D-1 | Demo Mode walkthrough | Stakeholder sign-off scope |

### Tuần 1 — Triển khai onsite

| Ngày | Hoạt động | Deliverable |
|------|-----------|-------------|
| D1 | Cài đặt production server tại trại / edge | `deploymentCheck.js` pass |
| D1 | Setup Wizard: Farm → Camera → Zone | 3 camera online |
| D2 | Uniform + workflow cơ bản | Rule test pass |
| D3 | Test zone từng camera | Biên bản overlay OK |
| D4 | Go-live giám sát (shadow mode) | Event log, không cảnh báo ngoài |
| D5 | Bật cảnh báo chính thức | Dashboard realtime |

### Tuần 2–4 — Vận hành song song

- Ban ATSH đối chiếu event vs thực tế (sampling 20 case/tuần)
- Fine-tune zone polygon, threshold uniform
- Weekly report: violations by type, top zones, compliance score
- Hotfix config qua export/import (không downtime)

### Tuần 5–6 — Đánh giá

| Hạng mục | Phương pháp |
|----------|-------------|
| Độ chính xác | Sample 50 events, tính precision/recall thủ công |
| False positive | Đếm event bị đóng “không vi phạm” |
| Latency | Thời gian camera → dashboard (target <30s) |
| UX | Phỏng vấn 3–5 người dùng |

### Tuần 7–8 — Quyết định mở rộng

- Báo cáo pilot (template mục 6)
- Roadmap phase 2: thêm camera, thêm farm, SLA
- Chốt pricing & hợp đồng (xem [AMS_PRICING_MODEL.md](./AMS_PRICING_MODEL.md))

---

## 4. Vai trò & trách nhiệm (RACI)

| Hoạt động | AMS Team | IT Trại | Ban ATSH | Quản lý trại |
|-----------|----------|---------|----------|--------------|
| Cài server AMS | R/A | C | I | I |
| Cấu hình camera RTSP | C | R/A | I | I |
| Vẽ zone / uniform | R/A | C | C | I |
| Xử lý vi phạm hàng ngày | C | I | R/A | I |
| Quyết định go-live | C | I | C | R/A |

*R = Responsible, A = Accountable, C = Consulted, I = Informed*

---

## 5. Checklist kỹ thuật trước go-live

### Hạ tầng

- [ ] Server đủ CPU/RAM (xem Deployment Guide)
- [ ] PostgreSQL + Redis chạy ổn định
- [ ] FFmpeg cài và test RTSP từng camera
- [ ] Backup DB + export AMS config
- [ ] HTTPS (nếu truy cập từ ngoài LAN)

### Cấu hình AMS

- [ ] Setup Wizard 5/5 bước hoàn tất
- [ ] `/api/health` → ok/degraded
- [ ] Zone test pass trên 100% camera pilot
- [ ] Rule test pass cho rule đang bật
- [ ] WebSocket realtime trên dashboard
- [ ] `DEMO_MODE=false`
- [ ] Đổi mật khẩu admin mặc định
- [ ] Tạo FARM_ADMIN (không dùng chung SUPER_ADMIN)

### Vận hành

- [ ] Quy trình xử lý event: ai nhận, SLA phản hồi
- [ ] Lịch review evidence hàng tuần
- [ ] Liên hệ escalation khi camera offline >2h

---

## 6. Báo cáo kết thúc pilot (template)

```markdown
# AMS Pilot Report — [Tên trại] — [Tháng/Năm]

## Executive Summary
- Thời gian pilot: [dates]
- Camera: [N] · Events: [N] · Compliance score TB: [%]

## Kết quả định lượng
| Metric | Target | Actual |
|--------|--------|--------|
| Uptime | 99% | |
| Event precision (sample) | ≥80% | |
| Setup time | ≤1 ngày | |
| User adoption | ≥3 users/day | |

## Top violations (7 ngày cuối)
1. ...
2. ...

## Vấn đề & khuyến nghị
- ...

## Quyết định
[ ] Mở rộng production  [ ] Gia hạn pilot  [ ] Dừng
```

---

## 7. Rủi ro & giảm thiểu

| Rủi ro | Mức | Giảm thiểu |
|--------|-----|------------|
| Camera offline do mạng | Cao | VLAN riêng, UPS switch PoE |
| False positive zone | Trung bình | Test zone 3 ngày shadow mode |
| Kháng cự thay đổi quy trình | Trung bình | Training + champion nội bộ |
| Thiếu GPU cho scale | Thấp (pilot) | Giới hạn 9 camera, sub-stream |
| Mất dữ liệu | Thấp | Backup DB + retention policy |

---

## 8. Demo Mode trong giai đoạn pre-pilot

Trước khi lắp camera thật, dùng Demo Mode để:

- Training Ban ATSH trên dashboard
- Stakeholder demo không cần RTSP
- UAT quy trình xử lý event

```env
DEMO_MODE=true
```

Farm demo: **Mind Farm Demo** — Nhà tắm, Cổng trại, Hàng rào.

Tắt demo trước go-live pilot thật.

---

## 9. Tài liệu liên quan

- [AMS_DEPLOYMENT_GUIDE.md](./AMS_DEPLOYMENT_GUIDE.md)
- [AMS_SOLUTION_OVERVIEW.md](./AMS_SOLUTION_OVERVIEW.md)
- [CAMERA_SETUP.md](../CAMERA_SETUP.md)
- [AMS_PRICING_MODEL.md](./AMS_PRICING_MODEL.md)
