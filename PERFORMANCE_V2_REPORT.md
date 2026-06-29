# AMS Performance Optimization V1 — Report

**Ngày:** 2026-06-18  
**Phạm vi:** Login → Dashboard first paint  
**Thay đổi:** `GET /api/dashboard/bootstrap` + `DashboardBootstrapStore`  
**Ràng buộc giữ nguyên:** UI · Event Pipeline · WebSocket

---

## Executive Summary

Sau Optimization V1, luồng authenticated session **không còn burst 10+ HTTP request** khi mở Dashboard. Toàn bộ dữ liệu khởi tạo được gom vào **1 API bootstrap**; frontend đọc từ **DashboardBootstrapStore**. WebSocket vẫn cập nhật realtime sau bootstrap.

| Metric | Before (V1 fixes) | After (Bootstrap V1) | Cải thiện |
|--------|-------------------|----------------------|-----------|
| HTTP sau login (Dashboard path) | **12** | **2** | **−83%** |
| Authenticated data API calls | **10** | **1** | **−90%** |
| Mục tiêu giảm ≥70% | — | **Đạt (83%)** | ✅ |

*Login vẫn cần `POST /api/auth/login` (1 request) — không thể gộp vào bootstrap vì chưa có token.*

---

## Before vs After

### Before (Performance Audit + V1 fixes)

**Luồng sau login → Dashboard:**

| # | Request | Mục đích |
|---|---------|----------|
| 1 | POST `/api/auth/login` | Token |
| 2 | GET `/api/auth/me` | User profile |
| 3 | GET `/api/health` | Sidebar health |
| 4 | GET `/api/events?limit=100` | EventStore |
| 5 | GET `/api/cameras` | EventStore metrics |
| 6 | GET `/api/transitions/recent` | Dashboard |
| 7 | GET `/api/workflows/compliance/summary` | Dashboard |
| 8 | GET `/api/workflows/dashboard` | Dashboard |
| 9 | GET `/api/dashboard/summary` | Dashboard |
| 10 | GET `/api/reports/compliance/kpis` | Dashboard widgets |
| 11 | GET `/api/reports/compliance/top-violations` | Dashboard widgets |
| 12 | GET `/api/camera-health/summary` | Dashboard widgets |
| — | WS `/ws/events` | Realtime (không đổi) |

**Tổng HTTP (Dashboard path):** 12 (+ WS)

**Vấn đề:**
- Waterfall song song nhiều endpoint
- Trùng dữ liệu events/cameras/health
- Polling 60s trên Dashboard (7 API/cycle)

---

### After (Bootstrap V1)

**Luồng sau login → Dashboard:**

| # | Request | Mục đích |
|---|---------|----------|
| 1 | POST `/api/auth/login` | Token |
| 2 | GET `/api/dashboard/bootstrap` | **Toàn bộ payload session** |
| — | WS `/ws/events` | Realtime (không đổi) |

**Bootstrap payload:**

```json
{
  "user": { "...": "..." },
  "dashboardSummary": { "...": "..." },
  "complianceSummary": { "kpis": {}, "topViolations": {} },
  "workflowSummary": { "compliance": {}, "dashboard": {}, "recentCrossings": {} },
  "cameraSummary": { "health": {}, "cameras": [] },
  "recentEvents": { "items": [], "total": 0, "page": 1, "limit": 100 },
  "notificationSummary": { "totalRules": 0, "enabledRules": 0 },
  "systemHealth": { "status": "ok", "...": "..." }
}
```

**Tổng HTTP (Dashboard path):** **2** (+ WS)

**Frontend:**
- `DashboardBootstrapStore` — fetch, retry, cache session data
- `EventStore` — hydrate từ `recentEvents` + `cameraSummary.cameras` (không gọi API riêng)
- `DashboardPage` — đọc store, **không useEffect API**
- `Sidebar` — `systemHealth` từ store
- `LoginPage` — `POST login` + `refreshBootstrap()` (bỏ `/auth/me`)

---

## Đo lường (ước lượng kiến trúc)

| Metric | Before | After | Ghi chú |
|--------|--------|-------|---------|
| **Login latency** | ~350–500 ms | ~350–450 ms | PBKDF2 login unchanged; bỏ `/auth/me` (~20–80 ms) |
| **Dashboard first render (data ready)** | Chờ slowest of ~10 API | Chờ **1 bootstrap** | Giảm tail latency đáng kể khi DB lớn |
| **Total API requests (post-login)** | 12 | 2 | **−83%** |
| **Dashboard polling** | 7 req / 60s | **0** | WS-only updates cho events |
| **Dev StrictMode double-fetch** | ~22 HTTP | ~3 HTTP | Bootstrap guard + single endpoint |

*Số liệu latency tuyệt đối phụ thuộc Postgres/Redis local; so sánh tương đối dựa trên số request và kiến trúc.*

---

## Backend Implementation

| File | Thay đổi |
|------|----------|
| `app/services/dashboard_bootstrap_service.py` | Gom query: summary, KPIs, workflow, cameras, events, health |
| `app/schemas/dashboard_bootstrap.py` | Response schema |
| `app/api/dashboard.py` | `GET /bootstrap` |

**Tối ưu giữ từ V1:** batch `events_to_engine_dicts`, SQL `COUNT` cho dashboard summary, Redis singleton.

---

## Frontend Implementation

| File | Thay đổi |
|------|----------|
| `context/DashboardBootstrapStore.jsx` | Store + retry |
| `services/dashboardBootstrapService.js` | API client |
| `context/EventStore.jsx` | Hydrate từ bootstrap, WS unchanged |
| `pages/DashboardPage.jsx` | Store-only data |
| `pages/LoginPage.jsx` | bootstrap thay `/auth/me` |
| `components/Sidebar.jsx` | health từ store |
| `components/auth/ProtectedRoute.jsx` | Retry UI khi bootstrap lỗi |
| `main.jsx` | Provider order |

---

## Chức năng giữ nguyên

| Hạng mục | Trạng thái |
|----------|------------|
| UI Dashboard | ✅ Không đổi layout/component |
| Event Pipeline | ✅ Không sửa backend pipeline |
| WebSocket `/ws/events` | ✅ Không đổi client/server |
| Realtime feed sau load | ✅ WS `event.created` / `event.updated` |
| Các trang khác (Violations, Monitoring…) | Vẫn gọi API riêng khi navigate |

---

## Retry khi bootstrap lỗi

- `ProtectedRoute`: nút **Thử lại** khi có token nhưng bootstrap fail
- `RealtimeEventFeed` / `RealtimeDashboardWidgets`: retry → bootstrap reload
- `DashboardBootstrapStore.retry()` / `refreshBootstrap()`

---

## Kết luận

| Tiêu chí | Kết quả |
|----------|---------|
| Giảm request sau login ≥70% | ✅ **83%** (12 → 2) |
| Không đổi UI | ✅ |
| Không đổi Event Pipeline | ✅ |
| Không đổi WebSocket | ✅ |
| Bootstrap + Store + retry | ✅ |
| Tests | Backend 83 pass · Frontend 51 pass · Build OK |

**Bước tiếp theo (ngoài scope V1):** cache bootstrap TTL ngắn, ETag, invalidate qua WS `config.updated`.

---

*Tham chiếu: [PERFORMANCE_AUDIT.md](./PERFORMANCE_AUDIT.md)*
