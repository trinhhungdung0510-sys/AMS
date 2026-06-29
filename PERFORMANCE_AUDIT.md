# AMS Performance Audit

**Ngày audit:** 2026-06-18  
**Phạm vi:** Login → Dashboard (cold start sau đăng nhập)  
**Phương pháp:** Static code analysis · trace request chain · review React lifecycle · backend query patterns  
**Ràng buộc:** Không sửa code · không thêm tính năng · không refactor

**Commit tham chiếu:** `3e7ce33` (`main`)

---

## Executive Summary

Nguyên nhân chính gây chậm khi **đăng nhập** và **mở Dashboard** nằm ở **backend**: endpoint `GET /api/events` tải toàn bộ bảng `events` kèm **N+1 query** khi localize từng event, cộng với **mở kết nối Redis trên mọi request có auth**. Frontend góp thêm bằng **burst ~10–12 HTTP request** khi mount Dashboard, **4 request không gửi token** (401 nhanh nhưng lãng phí và thiếu dữ liệu), **polling 15s** gọi lại gần như toàn bộ, và **EventStore re-render** lan sang nhiều component.

| Metric | Giá trị ước lượng |
|--------|-------------------|
| HTTP requests sau login → Dashboard | **10–12** (dev StrictMode: **~18–22**) |
| Request có auth (Redis overhead mỗi lần) | **6–7** |
| Request Dashboard dùng `fetch()` thiếu token | **4** |
| Polling Dashboard | **7 request / 15 giây** |
| DB queries cho `GET /events` (N events) | **1 + 3N** (zone + camera + farm / event) |
| WebSocket reconnect loop | **Không** (chỉ reconnect khi socket đóng) |

---

## 1. Luồng API sau Login

### 1.1 Login (`LoginPage.jsx`)

| # | Method | Endpoint | Auth | Ghi chú |
|---|--------|----------|------|---------|
| 1 | POST | `/api/auth/login` | Không | `pbkdf2_hmac` 120.000 vòng · audit log · `db.commit` |
| 2 | GET | `/api/auth/me` | Bearer | Redis blacklist check · AUTH DEBUG log |

**Không gọi trùng `/auth/me` từ `AuthContext`** khi submit form (context chỉ load token lúc app mount). Login flow gọn **2 request**.

### 1.2 App shell mount (`AppLayout` — mọi trang protected)

| # | Method | Endpoint | Auth | Ghi chú |
|---|--------|----------|------|---------|
| 3 | GET | `/api/health` | Không | `Sidebar.jsx` · deployment health report |

Health check backend (`deployment_health_service.build_health_report`):
- `SELECT 1` (DB)
- Redis `PING` (connection mới)
- Disk usage (`shutil.disk_usage`)
- `which ffmpeg` / `which ffprobe`
- Load toàn bộ `Camera` + `CameraHealth`

→ **Nặng hơn health check thông thường**, chạy mỗi lần mở layout.

### 1.3 EventStore init (`EventStore.jsx` — sau khi `user` set)

| # | Method | Endpoint | Auth | Ghi chú |
|---|--------|----------|------|---------|
| 4 | GET | `/api/events` | Bearer | **Không pagination** → full table |
| 5 | GET | `/api/cameras` | Bearer | List cameras theo farm scope |

Song song qua `Promise.all` trong `reload()`.

### 1.4 Dashboard mount (`DashboardPage.jsx`)

| # | Method | Endpoint | Auth | Ghi chú |
|---|--------|----------|------|---------|
| 6 | GET | `/api/transitions/recent?limit=8` | **Thiếu** | Raw `fetch()` — **401** |
| 7 | GET | `/api/workflows/compliance/summary` | **Thiếu** | Raw `fetch()` — **401** |
| 8 | GET | `/api/workflows/dashboard` | **Thiếu** | Raw `fetch()` — **401** |
| 9 | GET | `/api/dashboard/summary` | **Thiếu** | Raw `fetch()` — **401** |
| 10 | GET | `/api/reports/compliance/kpis` | Bearer | Load events hôm nay (filtered) |
| 11 | GET | `/api/reports/compliance/top-violations?days=7&limit=10` | Bearer | Load events 7 ngày (filtered) |
| 12 | GET | `/api/camera-health/summary` | Bearer | Load `CameraHealth` + `Camera` |

**WebSocket:** `subscribeWsEvents` → `/ws/events` (shared client, 1 connection).

### 1.5 Tổng burst lần đầu mở Dashboard

```
Login:     POST /auth/login + GET /auth/me
Layout:    GET /api/health
EventStore: GET /events + GET /cameras
Dashboard: 4× fetch (401) + 3× reports/health (200)
WS:         1× /ws/events
────────────────────────────────────────
≈ 12 HTTP + 1 WS
```

**React StrictMode (dev):** `useEffect` chạy **2 lần** → request có thể **gấp đôi** (~22 HTTP). Production build **không** double-mount.

---

## 2. Thời gian phản hồi từng API (ước lượng)

Không đo live (Postgres/server không chạy trong session audit). Ước lượng dựa trên pattern query + payload.

| Endpoint | Ước lượng (DB nhỏ <1k events) | Ước lượng (DB lớn 10k+ events) | Bottleneck chính |
|----------|-------------------------------|--------------------------------|------------------|
| POST `/auth/login` | 150–400 ms | 150–400 ms | PBKDF2 120k iterations |
| GET `/auth/me` | 20–80 ms | 20–80 ms | Redis connect + SELECT user |
| GET `/api/health` | 50–200 ms | 50–200 ms | Redis + disk + ffmpeg + cameras |
| **GET `/api/events`** | **200 ms – 2 s** | **5–30+ s** | Full scan + **3N DB queries** |
| GET `/api/cameras` | 30–100 ms | 50–200 ms | Redis auth + list cameras |
| GET `/api/dashboard/summary` | 100–500 ms | 2–10 s | Load **ALL** events + farms + cameras |
| GET `/api/workflows/compliance/summary` | 50–300 ms | 200 ms – 1 s | Progress rows + violations + zone lookup |
| GET `/api/workflows/dashboard` | 30–200 ms | 100–500 ms | Today's workflow violations |
| GET `/api/transitions/recent` | 20–100 ms | 50–200 ms | Indexed query, limit 8 |
| GET `/api/reports/compliance/kpis` | 50–300 ms | 500 ms – 3 s | `_load_events` today |
| GET `/api/reports/compliance/top-violations` | 100–500 ms | 1–5 s | `_load_events` 7 days |
| GET `/api/camera-health/summary` | 30–100 ms | 50–200 ms | 2 full table scans (small) |

**Overhead cố định mỗi request có auth:** `get_current_user` → Redis `from_url` + `GET jwt:blacklist:{jti}` + AUTH DEBUG `warning` log ≈ **10–50 ms/request** (phụ thuộc Redis latency).

---

## 3. API gọi trùng lặp

| Dữ liệu | Nơi gọi trùng | Mức độ |
|---------|---------------|--------|
| **Events** | EventStore `/events` + Dashboard `/dashboard/summary` + reports KPIs + top-violations + workflow panels | **Cao** |
| **Cameras** | EventStore `/cameras` + `/camera-health/summary` + `/api/health` camera check | **Trung bình** |
| **Workflow violations** | `/workflows/compliance/summary` + `/workflows/dashboard` (overlap `recent_violations` / `chi_tiet_hom_nay`) | **Trung bình** |
| **Metrics KPI** | `RealtimeDashboardWidgets` + `DashboardPage` stat-grid — cùng `useEventStore().metrics` | **Render trùng, 1 API** |
| **Auth profile** | Login `/auth/me` only once per login | **Không trùng** |

Backend reports: `build_dashboard_kpis` và `build_top_violations` là **2 query events riêng** dù gọi song song từ frontend.

---

## 4. Request loop

| Pattern | Có loop? | Chi tiết |
|---------|----------|----------|
| Dashboard `useEffect` deps `[]` | **Không** | Chạy 1 lần mount (+ StrictMode dev) |
| Dashboard `setInterval` 15s | **Polling cố ý** | 7 API mỗi 15s — không phải bug loop |
| EventStore `reload` on `[user]` | **Không** | Chỉ khi user thay đổi |
| AuthContext `loadUser` | **Không** | Chỉ mount |
| WS `scheduleReconnect` | **Không loop vô hạn nếu OK** | Chỉ khi socket close/error |

**Không phát hiện infinite request loop** trong code. Có **polling 15s** trên Dashboard — gây tải liên tục, không phải runaway loop.

---

## 5. WebSocket reconnect

File: `src/services/wsClient.js`

| Hành vi | Kết luận |
|---------|----------|
| Shared singleton `getSharedWsClient()` | 1 client toàn app |
| Reconnect | Exponential backoff 3s → max 30s |
| Trigger | `onclose` / `onerror` only |
| Reconnect liên tục khi server OK | **Không** |

EventStore subscribe qua `client.subscribe()` — **không tạo socket mới** mỗi render.

**Rủi ro:** Nếu backend WS không available → reconnect mỗi 3–30s → CPU/network nhẹ, UI hiển thị "Reconnecting...".

---

## 6. React component render nhiều lần

| Component | Trigger re-render | Mức ảnh hưởng |
|-----------|-------------------|---------------|
| `EventStoreProvider` | Mỗi `setEvents`, `setCameras`, WS `applyEvent`, `setConnected` | **Cao** — toàn subtree |
| `DashboardPage` | `useEventStore().metrics` thay đổi | **Trung bình** — full page + Recharts |
| `RealtimeDashboardWidgets` | Cùng EventStore | **Trung bình** — duplicate widgets |
| `RealtimeEventFeed` | `feedEvents` (max 50) mỗi WS event | **Trung bình** — list 50 items |
| `NotificationProvider` | `lastWsEvent` mỗi WS event | **Thấp–Trung bình** |
| `Sidebar` | Health state only | **Thấp** |

**StrictMode (dev):** double mount → double initial API burst.

**Recharts:** 2× `ResponsiveContainer` (LineChart + PieChart) — layout/measure pass tốn main thread khi Dashboard paint.

---

## 7. useEffect chạy lặp

| File | Effect | Deps | Lặp? |
|------|--------|------|------|
| `AuthContext.jsx` | `loadUser` | `[]` | Chỉ mount |
| `EventStore.jsx` | `reload` | `[authLoading, user, reload]` | Khi user login |
| `EventStore.jsx` | WS subscribe | `[user, applyEvent]` | Khi user login |
| `DashboardPage.jsx` | load + 2× interval | `[]` | Mount + poll 15s |
| `Sidebar.jsx` | `fetchApiHealth` | `[]` | Chỉ mount |
| `NotificationProvider.jsx` | toast on WS | `[lastWsEvent, ...]` | Mỗi WS event |

**Không có useEffect thiếu deps gây loop vô hạn.** Polling 15s là nguyên nhân lặp **cố ý**.

---

## 8. EventStore → Dashboard re-render

```
WS event / reload()
    → setEvents()
    → metrics = useMemo(events, cameras)  // recalc
    → value = useMemo(...)                 // new context object
    → Consumers re-render:
         DashboardPage (metrics)
         RealtimeDashboardWidgets (metrics, feedEvents, connected, loading)
         RealtimeEventFeed (feedEvents)
         NotificationProvider (lastWsEvent)
         FarmControlDashboardPage (if open)
```

**Kết luận:** **Có.** Mỗi event WS (demo mode có thể vài event/giây) gây **re-render toàn bộ Dashboard subtree** dù `DashboardPage` chỉ cần `metrics` (4 số). `feedEvents` thay đổi kéo theo `RealtimeDashboardWidgets` list re-render.

`applyEvent` còn gọi `sortEventsByTime` + slice 500 → **O(n log n)** mỗi event.

---

## 9. Polling không cần thiết

| Nguồn | Interval | Requests/cycle | Cần thiết? |
|-------|----------|----------------|------------|
| `DashboardPage` crossings | 15s | 1 | Có thể thay WS / gộp |
| `DashboardPage` workflow batch | 15s | 6 | **Trùng** với lần load đầu · có WS |
| `SystemStatusPage` | 15s | 1 | Hợp lý cho ops page |
| `MonitoringPage` cameras | 10s | 1 | Hợp lý |
| `FarmControlDashboardPage` | 30s | 1+ | Hợp lý |

Dashboard poll **6 endpoint reports/workflow** trong khi đã có EventStore + WS → **polling dư thừa** cho realtime metrics.

---

## 10. Database query chậm

### P0 — Critical

**`GET /api/events` (default, không query params)**

```python
# backend/app/api/events.py L47-48
events = list(db.scalars(select(Event).order_by(...)))
return [event_to_vi_dict(db, event) for event in events]
```

**`event_to_vi_dict`** mỗi event:
- `resolve_zone_name` → `SELECT FarmZone`
- `resolve_camera_name` → `SELECT Camera`
- `resolve_farm_name` → `SELECT Farm`

→ **1 + 3N queries**, payload JSON lớn, parse JSON phía client chậm.

### P1 — High

| Query location | Pattern | Vấn đề |
|----------------|---------|--------|
| `dashboard.py` `/summary` | `select(Event)` full table | Scan toàn bộ events |
| `atsh_biosecurity_engine.get_atsh_violation_summary` | All ATSH category events | Full scan + gọi từ dashboard summary |
| `compliance_report_service._load_events` | Filtered but no LIMIT | 7-day top violations có thể lớn |
| `get_current_user` | Redis new connection/request | Latency tích lũy × số API |
| `workflow_engine.get_compliance_summary` | `select(TrackWorkflowProgress)` all rows | Scale theo tracks |

### P2 — Medium

| Query | Ghi chú |
|-------|---------|
| `camera_health/summary` | 2 scans, bảng nhỏ |
| `transitions/recent` | Có LIMIT, OK |
| Login audit + commit | 1 transaction, OK |

**Index:** `Event.occurred_at`, `Event.event_type`, `Event.category` được filter nhưng full-list endpoints **không dùng pagination**.

---

## Top 10 Bottleneck

| # | Bottleneck | Ảnh hưởng | Triệu chứng | Priority |
|---|------------|-----------|-------------|----------|
| 1 | **`GET /api/events` full table + N+1 localize** | **Critical** | Dashboard đợi EventStore; TTFB tăng tuyến tính theo số event | **P0** |
| 2 | **Redis connect mỗi authenticated request** | **High** | 6–7 API sau login đều +10–50ms; tích lũy 100–350ms | **P0** |
| 3 | **Burst 10–12 HTTP khi mở Dashboard** | **High** | Waterfall + main thread busy; cảm giác "đơ" sau login | **P0** |
| 4 | **4 Dashboard `fetch()` thiếu Bearer token** | **High** | 401 → panels trống; vẫn tốn round-trip; user thấy "Chưa tải được" | **P0** |
| 5 | **Trùng load events** (EventStore + reports + dashboard summary) | **High** | DB & network x3–5 cho cùng dữ liệu | **P1** |
| 6 | **Polling 15s × 7 API trên Dashboard** | **Medium–High** | Tải liên tục; conflict với WS realtime | **P1** |
| 7 | **EventStore re-render cascade mỗi WS event** | **Medium–High** | Dashboard giật khi demo/live nhiều event | **P1** |
| 8 | **`GET /api/health` nặng trên Sidebar mount** | **Medium** | Chạy mọi trang, không cache | **P1** |
| 9 | **Login PBKDF2 120k + AUTH DEBUG logging** | **Medium** | Login 150–400ms; log I/O mỗi auth | **P2** |
| 10 | **Recharts + bundle JS ~855KB** | **Medium** | First paint Dashboard chậm sau data load | **P2** |

---

## Đề xuất tối ưu (chưa thực hiện)

### P0 — Làm trước (impact lớn, effort vừa)

1. **`GET /api/events`:** Thêm pagination mặc định (`limit=50–100`); EventStore chỉ fetch trang đầu + WS cho realtime. Bỏ N+1: batch load zone/camera/farm hoặc JOIN.
2. **Redis:** Connection pool singleton; cache blacklist check; bỏ `get_redis_client()` open/close mỗi request.
3. **Dashboard fetch:** Thay raw `fetch()` bằng `apiFetch()` (4 endpoint workflow/dashboard/transitions).
4. **Gộp burst:** Single endpoint `/api/dashboard/bootstrap` hoặc frontend `Promise.all` có auth + dedupe (1 lần events, không gọi summary trùng).

### P1 — Tuần tiếp theo

5. **Bỏ/giảm polling 15s** trên Dashboard; dùng WS `event.created` để invalidate metrics.
6. **`/api/dashboard/summary`:** SQL aggregate (`COUNT`, `GROUP BY`) thay vì load all events vào Python.
7. **EventStore:** Tách context (`MetricsStore` vs `FeedStore`) hoặc `useSyncExternalStore` selector để Dashboard không re-render khi `feedEvents` đổi.
8. **Sidebar health:** Cache 60s hoặc lazy-load sau first paint.
9. **Reports:** Merge KPI + top-violations thành 1 API hoặc shared query cache trong request.

### P2 — Cải thiện dài hạn

10. **Tắt AUTH DEBUG logs** trong production.
11. **Code-split** Recharts + route-based lazy load (`React.lazy`).
12. **StrictMode:** Chấp nhận dev 2×; verify production bundle không double-fetch.
13. **Login:** Giữ PBKDF2 nhưng hiển thị skeleton Dashboard ngay; defer non-critical widgets.
14. **`applyEvent`:** Insert sorted thay vì full sort 500 items mỗi WS message.

---

## Checklist audit (10 hạng mục)

| # | Hạng mục | Kết quả |
|---|----------|---------|
| 1 | API sau login | 2 (login) + 1 (health) + 2 (EventStore) + 7 (Dashboard) + WS ≈ **12** |
| 2 | Thời gian từng API | **`/events` dominant**; auth Redis overhead cố định |
| 3 | API trùng lặp | **Có** — events, cameras, workflow data |
| 4 | Request loop | **Không** — chỉ polling 15s cố ý |
| 5 | WS reconnect liên tục | **Không** khi server ổn |
| 6 | Component render nhiều | **Có** — EventStore consumers + Recharts |
| 7 | useEffect lặp | **Không** infinite; polling + StrictMode dev |
| 8 | EventStore → Dashboard re-render | **Có** — mỗi WS event |
| 9 | Polling không cần thiết | **Có** — Dashboard 15s × 7 |
| 10 | DB query chậm | **Có** — `/events` N+1, full scans |

---

## Phụ lục: File tham chiếu

| Vấn đề | File |
|--------|------|
| Login chain | `src/pages/LoginPage.jsx`, `src/context/AuthContext.jsx` |
| EventStore load | `src/context/EventStore.jsx`, `src/services/eventService.js` |
| Dashboard APIs | `src/pages/DashboardPage.jsx` |
| WS client | `src/services/wsClient.js` |
| Events API | `backend/app/api/events.py` |
| N+1 localize | `backend/app/services/vi_localization.py` |
| Auth Redis | `backend/app/api/deps.py` |
| Dashboard summary scan | `backend/app/api/dashboard.py` |
| Reports queries | `backend/app/services/compliance_report_service.py` |
| Health sidebar | `src/components/Sidebar.jsx`, `backend/app/services/deployment_health_service.py` |

---

## Fixes Applied (2026-06-18)

| Priority | Fix |
|----------|-----|
| P0 | `GET /api/events` — pagination mặc định `limit=100`, bỏ full table scan |
| P0 | Batch localize — `events_to_engine_dicts` / `LocalizationCache` (3 query thay vì 3N) |
| P0 | Redis singleton — `@lru_cache` client, không `close()` mỗi request |
| P0 | Dashboard — `apiFetch()` + Bearer cho 4 endpoint workflow/transitions |
| P0 | `/dashboard/summary` — SQL `COUNT` thay vì load all events |
| P1 | Dashboard polling — gộp 1 interval **60s** (was 15s × 7) |
| P1 | Sidebar health — cache 60s |
| P1 | Bỏ AUTH DEBUG `warning` logs (chỉ `debug` khi `environment=development`) |
| P1 | Bỏ stat-grid trùng trên Dashboard (giữ `RealtimeDashboardWidgets`) |
| P1 | EventStore — `getEvents({ limit: 100 })`, hỗ trợ engine + vi format |

---

*Báo cáo gốc — phân tích trước khi sửa. Xem mục Fixes Applied ở trên.*
