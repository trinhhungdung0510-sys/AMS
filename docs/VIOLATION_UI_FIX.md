# Sửa lỗi màn hình trắng — Vi phạm ATSH v1.7

Tài liệu báo cáo khắc phục lỗi UI tại tab **Vi phạm chưa xử lý** và **Vi phạm đã xử lý**.

**Phạm vi:** Frontend only — không thay đổi Backend, API, Database, Rule Engine.

---

## Hiện tượng

Khi mở trang `/vi-pham-atsh` và chuyển tab:

- **Vi phạm chưa xử lý**
- **Vi phạm đã xử lý**

Vùng nội dung chính có thể trắng hoàn toàn (React runtime error), thay vì hiển thị danh sách hoặc trạng thái trống.

---

## Nguyên nhân

| # | Nguyên nhân | Mô tả |
|---|-------------|--------|
| 1 | **`formatDateTime` không an toàn** | Gọi `date.split('-')` khi `date` là `undefined`/`null` → crash toàn bộ component tab |
| 2 | **Drawer nằm ngoài `BrowserRouter`** | `ViolationProcessingDrawer` render trong `ViolationProcessingProvider` (ngoài `App` router) nhưng dùng `<Link>` — lỗi React Router khi mở drawer |
| 3 | **Circular import Context ↔ Drawer** | `ViolationProcessingContext` import trực tiếp Drawer → rủi ro khởi tạo module không ổn định |
| 4 | **Thiếu null-guard trên mảng/metrics** | `feedEvents`, `openMetrics`, `resolvedRecords` có thể undefined trong nhịp render đầu → `.filter()` crash |
| 5 | **Không có Error Boundary** | Lỗi con làm trắng toàn bộ vùng tab, không có thông báo thân thiện |
| 6 | **Không có empty state rõ ràng** | Tab chưa xử lý trả về `null` khi rỗng thay vì hiển thị **"Chưa có dữ liệu."** |

---

## File đã sửa

| File | Thay đổi |
|------|----------|
| `src/utils/formatters.js` | `formatDateTime` an toàn với dữ liệu thiếu |
| `src/utils/formatters.test.js` | Test regression cho `formatDateTime` |
| `src/components/AtshViolationSnapshot.jsx` | Null-guard `violation` |
| `src/components/common/ErrorBoundary.jsx` | **Mới** — bắt lỗi render tab |
| `src/components/violations/OpenViolationsPanel.jsx` | **Mới** — tab chưa xử lý + empty state |
| `src/components/violations/ProcessedViolationsPanel.jsx` | Null-guard, format thời gian an toàn, empty state |
| `src/pages/ViolationsPage.jsx` | ErrorBoundary, tách tab, API fail-safe |
| `src/context/ViolationProcessingContext.jsx` | Guard mảng; bỏ render Drawer |
| `src/layouts/AppLayout.jsx` | Render `ViolationProcessingDrawer` trong Router |
| `src/components/violations/ViolationProcessingDrawer.jsx` | Guard `timeline` |
| `src/components/realtime/CollapsibleRealtimeEventPanel.jsx` | Guard `openFeedEvents`, empty text |
| `src/styles/ams-extensions.css` | Style notice / error boundary |

---

## Cách khắc phục

### 1. An toàn dữ liệu

- Mọi truy cập mảng dùng `(items ?? [])` hoặc `Array.isArray`.
- `formatDateTime` không gọi `.split` khi thiếu `date`.
- API load bọc `try/catch`; lỗi API → giữ mock + banner, **không crash**.

### 2. Kiến trúc Drawer

```
Trước: main.jsx → ViolationProcessingProvider → Drawer (ngoài Router) ❌

Sau:   AppLayout (trong Router) → ViolationProcessingDrawer ✅
       ViolationProcessingProvider chỉ quản lý state
```

### 3. Error Boundary

Tab content được bọc `ErrorBoundary`:

- Lỗi → thông báo thân thiện + nút **Thử lại**
- Sidebar / Header vẫn hiển thị

### 4. Empty state

| Trường hợp | Hiển thị |
|------------|----------|
| Tab chưa xử lý, không vi phạm OPEN | **Chưa có dữ liệu.** |
| Panel realtime rỗng | **Chưa có dữ liệu.** |
| Tab đã xử lý, chưa có lịch sử | **Chưa có dữ liệu.** |
| Có lịch sử nhưng lọc không khớp | Thông báo bộ lọc |

---

## Luồng sau khi sửa

```mermaid
flowchart TD
  A[/vi-pham-atsh] --> B{Tab?}
  B -->|chua-xu-ly| C[OpenViolationsPanel]
  B -->|da-xu-ly| D[ProcessedViolationsPanel]
  C --> E{ErrorBoundary}
  D --> E
  E -->|OK| F[Hiển thị dữ liệu / Chưa có dữ liệu]
  E -->|Lỗi| G[Thông báo + Thử lại]
  H[Click vi phạm] --> I[ViolationProcessingDrawer trong AppLayout]
```

---

## Xác nhận không ảnh hưởng Backend

| Hạng mục | Ảnh hưởng |
|----------|-----------|
| Backend / API | **Không đổi** |
| Database | **Không đổi** |
| WebSocket / EventStore | **Không đổi** |
| Rule Engine | **Không đổi** |

---

## Kết quả kiểm thử

```bash
npm test -- --run
npm run build
```

| Kiểm tra | Kết quả |
|----------|---------|
| `npm test -- --run` | **54/54** PASS |
| `npm run build` | PASS |
| Tab **Vi phạm chưa xử lý** | Mở được, empty state khi rỗng |
| Tab **Vi phạm đã xử lý** | Mở được, empty state khi rỗng |
| API lỗi / rỗng | Không crash, hiển thị mock hoặc **Chưa có dữ liệu.** |
| Error Boundary | Bắt lỗi render, không trắng toàn trang |

---

*TIN NGHIA AMS — UI ổn định, một trung tâm vi phạm duy nhất.*
