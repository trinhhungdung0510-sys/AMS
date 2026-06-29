# UI Menu AMS v1.7

Tài liệu mô tả tinh gọn và tổ chức lại menu điều hướng AMS cho hệ thống AI giám sát an toàn sinh học.

**Phạm vi:** Chỉ thay đổi giao diện Sidebar, vị trí hiển thị chức năng trên Dashboard và trang Vi phạm ATSH.

**Không thay đổi:** Backend, API, Database, Rule Engine, Workflow Engine, Compliance Engine, Route, phân quyền.

---

## Cấu trúc menu cũ

Menu phẳng, 14 mục, lẫn tiếng Anh và trùng nhóm chức năng:

| # | Nhãn hiển thị | Route |
|---|---------------|-------|
| 1 | Tổng quan | `/dashboard` |
| 2 | Bảng điều khiển | `/bang-dieu-khien` |
| 3 | Giám sát | `/monitoring` |
| 4 | Compliance Center | `/monitoring/compliance-center` |
| 5 | Tuân thủ ATSH | `/compliance` |
| 6 | Vi phạm ATSH | `/vi-pham-atsh` |
| 7 | Camera | `/camera` |
| 8 | Đồng phục | `/uniforms` |
| 9 | Quy tắc ATSH | `/quy-tac-atsh` |
| 10 | Setup Wizard | `/setup` |
| 11 | System Status | `/system-status` |
| 12 | Diagnostics | `/diagnostics` |
| 13 | Evidence | `/evidence` |
| 14 | Cài đặt | `/settings` |

**Vấn đề:**

- Trùng “Tổng quan” và “Bảng điều khiển”.
- Camera và Giám sát cùng cấp — khó thể hiện quan hệ cha/con.
- Tuân thủ ATSH tách khỏi Dashboard — người vận hành phải vào trang riêng để xem KPI chính.
- Bằng chứng và Vi phạm ATSH tách rời — tra cứu bằng chứng không liền mạch với xử lý vi phạm.
- Công cụ IT (setup, trạng thái, chẩn đoán) chiếm menu chính.

---

## Cấu trúc menu mới

Menu 4 nhóm, **100% tiếng Việt**, hỗ trợ thu gọn/mở rộng menu con:

### TỔNG QUAN

| Mục | Route |
|-----|-------|
| Bảng điều khiển | `/bang-dieu-khien` |

*Ghi chú:* Menu được tô sáng khi đang ở `/dashboard` (route mặc định sau login).

### GIÁM SÁT

| Mục | Route | Ghi chú |
|-----|-------|---------|
| Giám sát trực tiếp | `/monitoring` | Menu cha |
| └── Camera | `/camera` | Menu con |

### AN TOÀN SINH HỌC

| Mục | Route |
|-----|-------|
| Đồng phục | `/uniforms` |
| Quy tắc ATSH | `/quy-tac-atsh` |
| Vi phạm ATSH | `/vi-pham-atsh` |

### HỆ THỐNG

| Mục | Route |
|-----|-------|
| Cài đặt | `/settings` |

### Trong trang Cài đặt (ẩn khỏi Sidebar chính)

| Nhãn | Route cũ | Route |
|------|----------|-------|
| Hướng dẫn cài đặt | Setup Wizard | `/setup` |
| Trạng thái hệ thống | System Status | `/system-status` |
| Chẩn đoán hệ thống | Diagnostics | `/diagnostics` |

---

## Thay đổi chi tiết

### 1. Đổi tên menu

| Cũ | Mới |
|----|-----|
| Giám sát | **Giám sát trực tiếp** |

Route `/monitoring` và chức năng giữ nguyên.

### 2. Camera là menu con

Camera không còn hiển thị cấp 1. Nằm dưới **Giám sát trực tiếp** với nút thu gọn/mở rộng. Route `/camera` không đổi.

### 3. Bỏ “Tuân thủ ATSH” khỏi Sidebar

Route `/compliance` vẫn truy cập được (bookmark). Nội dung KPI chính được đưa lên **Bảng điều khiển** trong khối:

**TUÂN THỦ AN TOÀN SINH HỌC**

- Tỷ lệ tuân thủ (%)
- Số quy trình hoàn thành
- Số quy trình vi phạm
- Số vi phạm hôm nay
- Xu hướng 7 ngày

Dữ liệu lấy từ API hiện có: bootstrap (`workflowSummary`, `complianceSummary`), `/api/compliance/summary`, `/api/compliance/trends`. Khi chưa có dữ liệu hiển thị **“Chưa có dữ liệu”**.

### 4. Gộp “Bằng chứng” vào “Vi phạm ATSH”

Menu **Bằng chứng** ẩn khỏi Sidebar. Trang **Vi phạm ATSH** có tab:

- Danh sách vi phạm
- Bằng chứng
- Sự kiện (tab có sẵn)

Route `/evidence` vẫn hoạt động. Mỗi bằng chứng hiển thị: ảnh/snapshot, video (nếu có), camera, khu vực, thời gian, quy tắc vi phạm.

### 5. Cài đặt

Chỉ một mục **Cài đặt** trên Sidebar. Ba công cụ hệ thống nằm trong trang Cài đặt.

---

## Lý do thay đổi

1. **Đúng nghiệp vụ ATSH** — Nhóm Giám sát / An toàn sinh học / Hệ thống phản ánh quy trình vận hành trang trại.
2. **Giảm menu cấp 1** — Từ 10+ mục xuống 6 mục chính (+ 1 menu con Camera).
3. **Dashboard là điểm vào KPI** — Tuân thủ ATSH không cần trang sidebar riêng cho số liệu tổng hợp hàng ngày.
4. **Vi phạm và bằng chứng liền mạch** — Tab Bằng chứng trong cùng trung tâm vi phạm.
5. **Camera thuộc giám sát trực tiếp** — Phản ánh đúng quan hệ nghiệp vụ camera ↔ live monitoring.
6. **100% tiếng Việt** — Phù hợp người vận hành; chỉ mục đang chọn được tô màu cam.

---

## Xác nhận không ảnh hưởng nghiệp vụ

| Hạng mục | Ảnh hưởng |
|----------|-----------|
| Backend | **Không đổi** |
| API | **Không đổi** — Tận dụng `/api/compliance/*`, bootstrap, `/deployment/evidence` |
| Database | **Không đổi** |
| Rule / Workflow / Compliance Engine | **Không đổi** |
| Route | **Không đổi** — `/compliance`, `/evidence`, `/setup`, … vẫn truy cập được |
| Phân quyền | **Không đổi** |
| Compliance Center | Route `/monitoring/compliance-center` vẫn tồn tại, ẩn khỏi menu |

### File thay đổi (frontend)

| File | Thay đổi |
|------|----------|
| `src/components/Sidebar.jsx` | Menu mới, menu con Camera, thu gọn/mở rộng |
| `src/App.css` | Style submenu, khối tuân thủ, bằng chứng |
| `src/pages/DashboardPage.jsx` | Khối Tuân thủ an toàn sinh học |
| `src/components/dashboard/BiosecurityCompliancePanel.jsx` | Panel KPI + xu hướng 7 ngày |
| `src/pages/ViolationsPage.jsx` | Tab Bằng chứng |
| `src/components/evidence/EvidenceBrowserPanel.jsx` | Component dùng chung |
| `src/pages/SnapshotBrowserPage.jsx` | Dùng lại EvidenceBrowserPanel |

---

## Kiểm tra chất lượng

```bash
npm test -- --run
npm run build
```

Kết quả mong đợi: build thành công, test pass, mọi route hoạt động, không lỗi giao diện.

---

*TIN NGHIA AMS — AI giám sát an toàn sinh học trang trại heo.*
