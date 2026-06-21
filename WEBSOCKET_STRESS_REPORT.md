# WebSocket Stress Test Report

**Generated:** 2026-06-21T10:07:40.067527+00:00  
**Mode:** `pipeline`  
**Path:** EventBus → EventStreamService → `/ws/events`

## Summary

| Events | Received | Duration (s) | Throughput (evt/s) | Latency avg (ms) | Latency p95 (ms) | Latency p99 (ms) | Memory Δ (MB) | CPU avg (%) |
|--------|----------|--------------|--------------------|------------------|------------------|------------------|---------------|-------------|
| 1000 | 1000 | 0.2961 | 3376.73 | 254.255 | 274.992 | 275.212 | 21.39 | 0.26 |
| 5000 | 5000 | 0.4352 | 11488.52 | 223.665 | 381.899 | 383.105 | 21.42 | 0.39 |
| 10000 | 10000 | 0.954 | 10482.2 | 558.641 | 848.899 | 867.848 | 37.73 | 0.31 |

## Latency detail

### 1000 events

| Metric | ms |
|--------|-----|
| min | 65.98 |
| avg | 254.255 |
| p50 | 261.252 |
| p95 | 274.992 |
| p99 | 275.212 |
| max | 275.376 |

- Memory: 20.52 → 41.91 MB (Δ 21.39 MB)
- CPU avg (process): 0.26%

### 5000 events

| Metric | ms |
|--------|-----|
| min | 55.264 |
| avg | 223.665 |
| p50 | 233.69 |
| p95 | 381.899 |
| p99 | 383.105 |
| max | 396.197 |

- Memory: 39.41 → 60.83 MB (Δ 21.42 MB)
- CPU avg (process): 0.39%

### 10000 events

| Metric | ms |
|--------|-----|
| min | 200.8 |
| avg | 558.641 |
| p50 | 565.925 |
| p95 | 848.899 |
| p99 | 867.848 |
| max | 880.842 |

- Memory: 44.58 → 82.31 MB (Δ 37.73 MB)
- CPU avg (process): 0.31%

## Methodology

1. Publish `event.created` messages through in-process EventBus.
2. EventStreamService forwards to WebSocket broadcast handler.
3. Latency = WebSocket `send_json` receive time − publish monotonic time.
4. Memory/CPU measured on stress test process via psutil
.

## How to run

```bash
cd backend
python scripts/websocket_stress_test.py
python scripts/websocket_stress_test.py --live --api-url http://127.0.0.1:8000
```

## Interpretation

| Latency p95 | Assessment |
|-------------|------------|
| < 5 ms | Excellent (in-process) |
| 5–20 ms | Good |
| 20–100 ms | Acceptable under load |
| > 100 ms | Investigate WS fan-out / CPU saturation |

| Memory Δ | Assessment |
|----------|------------|
| < 50 MB per 10k events | Stable |
| 50–200 MB | Monitor for leak over time |
| > 200 MB | Review connection cleanup |

## Conclusions

- All scenarios delivered 100% of events. Max p95 latency 848.90 ms — review if live mode exceeds 100 ms.
- Peak memory delta across scenarios: 37.73 MB — stable.
- Pipeline mode validates EventBus → EventStreamService → WS handler without HTTP/DB overhead.
- For end-to-end numbers, run with `STRESS_TEST=true` and `--live` against a running server.
