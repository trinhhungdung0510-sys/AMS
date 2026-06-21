# AMS — Pricing Model

Mô hình giá tham khảo cho **AMS (Animal Management System) v2.0**. Số liệu dưới đây là **framework định giá** — cần điều chỉnh theo thị trường, quy mô triển khai và hợp đồng thực tế.

---

## 1. Nguyên tắc định giá

1. **Giá theo giá trị** — giảm rủi ro dịch bệnh, tăng khả năng audit ATSH
2. **Scale theo camera & farm** — chi phí biên tăng theo ingest video và storage
3. **Tách license vs dịch vụ** — phần mềm + triển khai + support tách dòng
4. **Pilot → Production** — ưu đãi pilot được khấu trừ một phần khi ký HĐ chính thức

---

## 2. Các gói sản phẩm

### Starter — Demo & Training

| Hạng mục | Nội dung |
|----------|----------|
| **Đối tượng** | Sales demo, training nội bộ, UAT |
| **Phạm vi** | Demo Mode, 1 farm ảo, không camera thật |
| **Giới hạn** | Không SLA, self-hosted |
| **Giá tham khảo** | **Miễn phí** (self-host) hoặc **$0–500/tháng** (hosted demo cloud) |

### Pilot — 1 trại thử nghiệm

| Hạng mục | Nội dung |
|----------|----------|
| **Đối tượng** | 1 farm, 3–9 camera, 30–60 ngày |
| **Bao gồm** | Triển khai onsite 1–2 ngày, training 2 buổi, support email |
| **Không bao gồm** | Hardware camera, server vật lý (có thể thuê) |
| **Giá tham khảo** | **$3,000 – $8,000** (one-time) + **$500 – $1,500/tháng** support pilot |

*Khấu trừ 50–100% phí pilot khi ký Professional trong 90 ngày.*

### Professional — Production single/multi farm

| Hạng mục | Nội dung |
|----------|----------|
| **Đối tượng** | 1–5 farm, ≤30 camera/farm |
| **Bao gồm** | License AMS, deployment kit, RBAC, reports, backup |
| **Support** | Email + ticket, SLA phản hồi 8×5, 24h |
| **Giá license (năm)** | **$12,000 – $36,000/năm** (theo số camera) |

### Enterprise — Chuỗi trại

| Hạng mục | Nội dung |
|----------|----------|
| **Đối tượng** | 5+ farm, central dashboard, audit compliance |
| **Bao gồm** | Multi-tenant, SSO (roadmap), dedicated support, custom SLA |
| **Giá license (năm)** | **$50,000+** — báo giá theo RFP |

---

## 3. Bảng giá theo camera (Professional)

Giá license software **hàng năm**, chưa VAT, chưa triển khai:

| Camera active | Giá/năm (USD) | Giá/camera/tháng |
|---------------|---------------|------------------|
| 1 – 5 | $12,000 | ~$200 |
| 6 – 15 | $24,000 | ~$133 |
| 16 – 30 | $36,000 | ~$100 |
| 31 – 60 | Báo giá | ~$80 |
| 61+ | Enterprise | Custom |

**Farm fee:** +$2,000/năm mỗi farm thêm (sau farm đầu tiên).

---

## 4. Dịch vụ triển khai (one-time)

| Dịch vụ | Mô tả | Giá tham khảo (USD) |
|---------|--------|---------------------|
| **Remote deployment** | Hướng dẫn qua call, khách tự lắp camera | $1,500 |
| **Onsite deployment** | 1–2 ngày tại trại, Setup Wizard, test zone | $3,000 – $5,000 |
| **Zone design workshop** | Vẽ zone + uniform với Ban ATSH | $1,000 – $2,000 |
| **Training** | 2 buổi (admin + vận hành) | $800 – $1,500 |
| **Migration / import config** | Import từ pilot hoặc site cũ | $1,000+ |

---

## 5. Support & maintenance

| Gói | SLA | Kênh | Giá/tháng (USD) |
|-----|-----|------|-----------------|
| **Standard** | Phản hồi 24h (8×5) | Email | $500 |
| **Business** | Phản hồi 8h (8×5) | Email + chat | $1,200 |
| **Premium** | Phản hồi 4h (12×6) | Dedicated channel | $2,500+ |

Bao gồm: cập nhật minor version, security patch, hỗ trợ troubleshooting.

**Không bao gồm:** onsite không lên lịch, custom feature development.

---

## 6. Add-ons (tùy chọn)

| Add-on | Mô tả | Giá tham khảo |
|--------|--------|---------------|
| **Extended retention** | Lưu evidence >90 ngày (180/365) | +$200–800/tháng theo TB |
| **Extra storage** | NAS / cloud backup evidence | Cost + 20% margin |
| **GPU inference node** | Server edge AI riêng | Hardware + $3,000 setup |
| **Custom report** | PDF branding, KPI tùy chỉnh | $2,000 – $5,000 |
| **SSO / LDAP** | Enterprise auth (roadmap) | Enterprise only |

---

## 7. Mô hình hosting

### Self-hosted (khách hàng)

- Khách cung cấp server, DB, network
- License fee theo bảng camera
- Triển khai + support tách dòng

### Managed cloud (vendor)

| Tier | Camera | Giá/tháng (USD) |
|------|--------|-----------------|
| Cloud S | ≤5 | $800 |
| Cloud M | ≤15 | $1,800 |
| Cloud L | ≤30 | $3,500 |

Bao gồm: VM, PostgreSQL managed, backup, monitoring cơ bản.

---

## 8. So sánh với chi phí không dùng AMS

| Hạng mục | Không AMS | Với AMS |
|----------|-----------|---------|
| Giám sát ATSH | Nhân sự 2–3 ca/ngày | Tự động 24/7 |
| Bằng chứng vi phạm | Không hệ thống | Snapshot + event ID |
| Audit dịch bệnh | Khó truy vết | Event catalog + audit log |
| Chi phí ước tính/năm | $40k–80k nhân công giám sát | $15k–36k license + triển khai |

*ROI phụ thuộc quy mô trại và chi phí sự cố dịch bệnh — thường breakeven 12–24 tháng cho trại ≥5,000 con.*

---

## 9. Điều khoản thương mại gợi ý

| Điều khoản | Gợi ý |
|------------|-------|
| Thanh toán license | 50% ký HĐ, 50% go-live |
| Pilot | 100% trước khi bắt đầu |
| Support | Trả trước theo quý/năm |
| Tăng camera | Prorate theo số camera thêm |
| Hủy | Không hoàn license năm; support cancel 30 ngày notice |

---

## 10. Bảng báo giá nhanh (ví dụ)

**Khách hàng:** Trại heo 1 site, 9 camera, pilot 60 ngày → production 1 năm

| Dòng | Số tiền (USD) |
|------|---------------|
| Pilot package (60 ngày) | $5,000 |
| Professional license (9 cam, 1 farm/năm) | $24,000 |
| Onsite deployment | $4,000 |
| Training (2 buổi) | $1,200 |
| Business support (12 tháng) | $14,400 |
| **Tổng năm 1** | **~$48,600** |
| Trừ pilot credit (nếu ký trong 90 ngày) | −$5,000 |
| **Net năm 1** | **~$43,600** |

---

## 11. Liên hệ báo giá

Báo giá chính thức cần:

- Số farm và camera
- Mô hình hosting (self / managed)
- Yêu cầu SLA và retention
- Lịch pilot / go-live

Tài liệu kèm: [AMS_BROCHURE.md](./AMS_BROCHURE.md) · [AMS_PILOT_PLAN.md](./AMS_PILOT_PLAN.md)

---

*Tài liệu mang tính tham khảo — không phải cam kết giá công bố. Phiên bản pricing: v2.0 · Cập nhật: 2026.*
