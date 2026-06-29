# Giao diện menu AMS v1.7

Tài liệu mô tả tinh gọn và Việt hóa menu điều hướng AMS cho người quản lý trang trại.

**Phạm vi:** Chỉ thay đổi giao diện menu sidebar và liên kết công cụ trong trang Cài đặt.

**Không thay đổi:** Route, API, database, backend, engine, quyền người dùng.

---

## Menu cũ

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

- Trùng “Tổng quan” và “Bảng điều khiển” gây khó chọn điểm vào chính.
- Nhiều nhãn tiếng Anh (Compliance Center, Setup Wizard, System Status, Diagnostics, Evidence).
- Công cụ vận hành (setup, trạng thái, chẩn đoán) chiếm menu chính — không phù hợp tần suất dùng hàng ngày.
- Không có nhóm nghiệp vụ rõ ràng cho quản lý trang trại.

---

## Menu mới

Menu 4 nhóm, 10 mục, **100% tiếng Việt**:

### TỔNG QUAN

| Mục | Route | Biểu tượng |
|-----|-------|------------|
| Bảng điều khiển | `/bang-dieu-khien` | Đồng hồ (`Gauge`) |

*Ghi chú:* Mục này cũng được tô sáng khi đang ở `/dashboard` (route mặc định sau login, không đổi route).

### GIÁM SÁT

| Mục | Route | Biểu tượng |
|-----|-------|------------|
| Giám sát | `/monitoring` | Màn hình (`Monitor`) |
| Camera | `/camera` | Camera (`Camera`) |

### AN TOÀN SINH HỌC

| Mục | Route | Biểu tượng |
|-----|-------|------------|
| Đồng phục | `/uniforms` | Áo (`Shirt`) |
| Quy tắc ATSH | `/quy-tac-atsh` | Danh sách (`ListChecks`) |
| Tuân thủ ATSH | `/compliance` | Khiên có dấu tích (`ShieldCheck`) |
| Vi phạm ATSH | `/vi-pham-atsh` | Khiên cảnh báo (`ShieldAlert`) |
| Bằng chứng | `/evidence` | Hình ảnh (`Image`) |

### HỆ THỐNG

| Mục | Route | Biểu tượng |
|-----|-------|------------|
| Cài đặt | `/settings` | Bánh răng (`Settings`) |

### Trong trang Cài đặt (không hiển thị menu chính)

| Nhãn mới | Nhãn cũ | Route |
|----------|---------|-------|
| Hướng dẫn cài đặt | Setup Wizard | `/setup` |
| Trạng thái hệ thống | System Status | `/system-status` |
| Chẩn đoán hệ thống | Diagnostics | `/diagnostics` |

---

## Lý do thay đổi

1. **Ngôn ngữ thống nhất** — Toàn bộ menu chính dùng tiếng Việt, phù hợp người vận hành trang trại.
2. **Nhóm theo nghiệp vụ** — Tổng quan → Giám sát → ATSH → Hệ thống, dễ quét và đào tạo.
3. **Giảm nhiễu** — Gom công cụ IT (setup, trạng thái, chẩn đoán) vào Cài đặt; bỏ Compliance Center khỏi menu chính.
4. **Bớt trùng lặp** — Chỉ còn một mục “Bảng điều khiển” thay cho cặp Tổng quan / Bảng điều khiển.
5. **Biểu tượng nhất quán** — Kích thước 20px, chỉ mục đang chọn có nền cam; khoảng cách đồng đều giữa các mục.

---

## Ảnh hưởng

| Hạng mục | Ảnh hưởng |
|----------|-----------|
| Route | **Không đổi** — Mọi URL cũ vẫn truy cập được (bookmark, link nội bộ). |
| API / Backend | **Không đổi** |
| Database | **Không đổi** |
| Quyền người dùng | **Không đổi** |
| Compliance Center | Route `/monitoring/compliance-center` **vẫn tồn tại**, chỉ **ẩn khỏi menu**. |
| Dashboard mặc định | `/` và `/dashboard` **vẫn hoạt động**; menu highlight “Bảng điều khiển” khi ở các trang này. |
| Cài đặt | Thêm khối “Công cụ hệ thống” với 3 liên kết nội bộ. |
| File thay đổi | `src/components/Sidebar.jsx`, `src/pages/SettingsPage.jsx`, `src/App.css` |

---

## Kiểm tra chất lượng

Sau triển khai v1.7:

```bash
npm test -- --run
npm run build
```

Kết quả mong đợi: không lỗi build, toàn bộ test frontend pass.

---

*TIN NGHIA AMS — AI giám sát an toàn sinh học trang trại heo.*
