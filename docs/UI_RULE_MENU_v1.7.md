# UI Rule Menu AMS v1.7

Tài liệu mô tả tối ưu cấu trúc menu **Quy tắc ATSH** và nhóm quy tắc trên giao diện AMS.

**Phạm vi:** Chỉ thay đổi Sidebar và giao diện trang Quy tắc ATSH / Đồng phục.

**Không thay đổi:** Backend, API, Database, Rule Engine, Workflow Engine, Compliance Engine, Route, phân quyền.

---

## Menu trước

Nhóm **AN TOÀN SINH HỌC** có 3 mục cấp 1:

| Mục | Route |
|-----|-------|
| Đồng phục | `/uniforms` |
| Quy tắc ATSH | `/quy-tac-atsh` |
| Vi phạm ATSH | `/vi-pham-atsh` |

Trang **Quy tắc ATSH** hiển thị danh sách phẳng tất cả quy tắc, không phân nhóm.

**Vấn đề:**

- Đồng phục là một loại quy tắc ATSH nhưng tách thành menu riêng — tăng số mục cấp 1.
- Người vận hành khó thấy quan hệ giữa đồng phục và quy tắc sai màu áo.
- Danh sách quy tắc dài khó quét khi số lượng tăng.

---

## Menu sau

Nhóm **AN TOÀN SINH HỌC** còn **2 mục cấp 1**:

| Mục | Route | Ghi chú |
|-----|-------|---------|
| Quy tắc ATSH | `/quy-tac-atsh` | Menu cha |
| └── Đồng phục | `/uniforms` | Menu con |
| Vi phạm ATSH | `/vi-pham-atsh` | — |

### Toàn bộ Sidebar v1.7 (sau thay đổi)

**TỔNG QUAN**

- Bảng điều khiển

**GIÁM SÁT**

- Giám sát trực tiếp
  - └── Camera

**AN TOÀN SINH HỌC**

- Quy tắc ATSH
  - └── Đồng phục
- Vi phạm ATSH

**HỆ THỐNG**

- Cài đặt

---

## Trang Quy tắc ATSH — nhóm quy tắc

Danh sách quy tắc được tổ chức theo nhóm có thể thu gọn/mở rộng:

| Nhóm | Quy tắc / Hành động |
|------|---------------------|
| Đồng phục | Liên kết quản lý đồng phục (`/uniforms`) + quy tắc sai màu áo |
| Rửa tay | Không sát trùng tay |
| Sát trùng ủng | Không sát trùng chân |
| Sát trùng xe | Xe chưa sát trùng, tiếp xúc xe cám/heo |
| Vùng cấm | Người/xe vào vùng cấm |
| Động vật xâm nhập | Chó, mèo, chuột, chim… |
| Các quy tắc khác | Không tắm, tiếp xúc người lạ, quy tắc chưa phân loại |

Nhóm mới có thể bổ sung trong `ATSH_RULE_GROUPS` (`src/data/atshRules.js`) mà không đổi API.

---

## Đồng phục

Route `/uniforms` và toàn bộ chức năng giữ nguyên:

- Uniform Template
- Quản lý mẫu đồng phục
- Gán đồng phục cho vùng
- Chỉnh sửa / Xóa / Xem trước

Chỉ thay đổi vị trí trên Sidebar (menu con) và liên kết từ nhóm **Đồng phục** trên trang Quy tắc ATSH.

---

## Lý do thay đổi

1. **Giảm menu cấp 1** — AN TOÀN SINH HỌC từ 3 xuống 2 mục chính.
2. **Đúng nghiệp vụ** — Đồng phục là một phần của quy tắc ATSH, không phải module độc lập.
3. **Dễ mở rộng** — Nhóm quy tắc accordion hỗ trợ thêm quy tắc mà không làm dài danh sách phẳng.
4. **100% tiếng Việt** — Nhãn menu và nhóm quy tắc thống nhất.

---

## Xác nhận không ảnh hưởng nghiệp vụ

| Hạng mục | Ảnh hưởng |
|----------|-----------|
| Backend | **Không đổi** |
| API | **Không đổi** — Vẫn dùng `/api/biosecurity-rules`, uniform API |
| Database | **Không đổi** |
| Rule Engine | **Không đổi** |
| Workflow / Compliance Engine | **Không đổi** |
| Route | **Không đổi** — `/uniforms`, `/quy-tac-atsh` vẫn truy cập trực tiếp |
| Phân quyền | **Không đổi** |

### File thay đổi (frontend)

| File | Thay đổi |
|------|----------|
| `src/components/Sidebar.jsx` | Đồng phục là menu con của Quy tắc ATSH |
| `src/data/atshRules.js` | `ATSH_RULE_GROUPS`, `groupAtshRules()` |
| `src/pages/AtshRulesPage.jsx` | Giao diện nhóm quy tắc accordion |
| `src/pages/UniformsPage.jsx` | Việt hóa tiêu đề trang |
| `src/styles/ams-extensions.css` | Style nhóm quy tắc |

---

## Kiểm tra chất lượng

```bash
npm test -- --run
npm run build
```

Kết quả mong đợi: build và test pass; route `/uniforms` và `/quy-tac-atsh` hoạt động bình thường.

---

*TIN NGHIA AMS — AI giám sát an toàn sinh học trang trại heo.*
