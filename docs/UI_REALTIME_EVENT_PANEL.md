# UI Realtime Event Panel

Tài liệu mô tả cải tiến bảng **Sự kiện Realtime** trên Dashboard AMS v1.7.

**Phạm vi:** Chỉ thay đổi giao diện hiển thị sự kiện trên Dashboard.

**Không thay đổi:** Backend, WebSocket, API, Event Pipeline, Event Store, Database, logic realtime.

---

## Giao diện cũ

Trên Dashboard (`RealtimeDashboardWidgets`):

- Khối **Realtime Dashboard** với trạng thái WS tiếng Anh.
- **4 thẻ KPI** (Event đang mở, Event nghiêm trọng, Sự kiện hôm nay, Camera online).
- Panel **Recent Events** luôn mở, hiển thị tối đa 5 sự kiện (chỉ tên + khu vực).
- Sidebar layout (`RealtimeEventFeed`) hiển thị thêm danh sách sự kiện bên phải — trùng lặp và chiếm nhiều diện tích.

**Vấn đề:**

- Dashboard bị kéo dài ngay cả khi người dùng không cần xem chi tiết sự kiện.
- Danh sách sự kiện hiển thị ở hai nơi trên cùng một trang.
- Thiếu thu gọn/mở rộng và điều khiển cuộn độc lập.

---

## Giao diện mới

Panel **SỰ KIỆN TRỰC TIẾP** có thể thu gọn / mở rộng.

### Trạng thái mặc định (Thu gọn)

Khi mở Dashboard, panel ở trạng thái thu gọn:

```
SỰ KIỆN TRỰC TIẾP
● Đang theo dõi
(25 sự kiện hôm nay)
                    [▼ Mở]
```

- Không hiển thị danh sách sự kiện.
- Chiều cao tối thiểu, không làm kéo dài Dashboard.

### Trạng thái mở rộng

Khi nhấn **Mở**:

- Animation mở/đóng **250ms** (`grid-template-rows`).
- Danh sách sự kiện realtime từ `EventStore` (WebSocket + bootstrap).
- Chiều cao danh sách cố định **400px**, thanh cuộn riêng (`overscroll-behavior: contain`).
- Sự kiện mới luôn ở **trên cùng** (giữ `sortEventsByTime` hiện có).
- Mỗi sự kiện hiển thị: **Mức độ** (badge màu), **Thời gian**, **Camera**, **Khu vực**, **Nội dung vi phạm**.
- Bấm vào sự kiện → chi tiết (`/vi-pham-atsh/:id` hoặc tab Sự kiện).

Header khi mở rộng:

- Tiêu đề **SỰ KIỆN TRỰC TIẾP**
- Số lượng sự kiện hôm nay (bên phải)
- Nút **▲ Thu gọn**

### Thanh cuộn thông minh

- Danh sách cuộn trong panel, **không cuộn toàn bộ Dashboard**.
- Người dùng ở **đầu danh sách** (đang theo dõi live): sự kiện mới hiển thị ngay.
- Người dùng đã cuộn xem sự kiện cũ: **giữ vị trí cuộn**, không tự kéo lên/xuống gây gián đoạn.

### Vị trí hiển thị

Panel **Sự kiện trực tiếp** hiển thị trên **mọi trang** (sidebar phải), thu gọn mặc định:

- Bảng điều khiển, Giám sát, Camera, Quy tắc ATSH, Đồng phục, Vi phạm ATSH, Cài đặt, …

Không còn bảng *Sự kiện realtime* cũ (luôn mở, tiếng Anh).

---

## Lý do thay đổi

1. **Giảm diện tích Dashboard** — Mặc định thu gọn, chỉ mở khi cần theo dõi chi tiết.
2. **Theo dõi realtime vẫn rõ ràng** — Trạng thái “Đang theo dõi” và số sự kiện hôm nay luôn hiển thị.
3. **Trải nghiệm cuộn tốt hơn** — Panel có chiều cao cố định, không làm nhảy bố cục trang.
4. **Thông tin sự kiện đầy đủ hơn** — Mức độ, thời gian, camera, khu vực, nội dung vi phạm.
5. **Bớt trùng lặp** — Một panel sự kiện trên Dashboard thay vì hai khu vực.

---

## Xác nhận không ảnh hưởng nghiệp vụ

| Hạng mục | Ảnh hưởng |
|----------|-----------|
| Backend | **Không đổi** |
| WebSocket / `wsClient` | **Không đổi** |
| API | **Không đổi** |
| Event Pipeline | **Không đổi** |
| Event Store (`EventStore.jsx`) | **Không đổi** — UI chỉ đọc `feedEvents`, `metrics`, `connected` |
| Database | **Không đổi** |
| Logic realtime | **Không đổi** — Vẫn subscribe WS và normalize qua `eventNormalizer` |

### File thay đổi (frontend)

| File | Thay đổi |
|------|----------|
| `src/components/realtime/CollapsibleRealtimeEventPanel.jsx` | Panel thu gọn/mở rộng mới |
| `src/components/realtime/RealtimeDashboardWidgets.jsx` | Dùng panel mới, bỏ KPI + Recent Events |
| `src/layouts/AppLayout.jsx` | Ẩn sidebar feed trên Dashboard |
| `src/styles/ams-extensions.css` | Style panel, animation, danh sách sự kiện |

---

## Kiểm tra chất lượng

```bash
npm test -- --run
npm run build
```

Kết quả mong đợi:

- Build và test frontend thành công.
- WebSocket vẫn cập nhật sự kiện qua `EventStore`.
- Dashboard ổn định bố cục khi thu gọn/mở rộng.

---

*TIN NGHIA AMS — AI giám sát an toàn sinh học trang trại heo.*
