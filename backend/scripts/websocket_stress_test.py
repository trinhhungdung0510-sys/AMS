#!/usr/bin/env python3
"""
AMS WebSocket stress test.

Publishes compliance events through EventBus → EventStreamService → /ws/events
and measures latency, CPU, and memory for 1000 / 5000 / 10000 events.

Usage:
  cd backend
  python scripts/websocket_stress_test.py
  python scripts/websocket_stress_test.py --live --api-url http://127.0.0.1:8000
  python scripts/websocket_stress_test.py --output ../WEBSOCKET_STRESS_REPORT.md
"""

from __future__ import annotations

import argparse
import asyncio
import gc
import json
import statistics
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


EVENT_COUNTS = (1000, 5000, 10000)


@dataclass
class ScenarioResult:
    event_count: int
    events_received: int
    duration_sec: float
    events_per_sec: float
    latency_min_ms: float
    latency_avg_ms: float
    latency_p50_ms: float
    latency_p95_ms: float
    latency_p99_ms: float
    latency_max_ms: float
    memory_before_mb: float
    memory_after_mb: float
    memory_delta_mb: float
    cpu_percent_avg: float
    errors: list[str] = field(default_factory=list)


class RecordingWebSocket:
    """Minimal WebSocket stand-in for in-process broadcast timing."""

    def __init__(self) -> None:
        self.latencies_ms: list[float] = []
        self.received_tags: set[str] = set()
        self._publish_times: dict[str, float] = {}

    def register_publish(self, tag: str, started_at: float) -> None:
        self._publish_times[tag] = started_at

    async def accept(self) -> None:
        return None

    async def send_json(self, message: dict[str, Any]) -> None:
        received_at = time.perf_counter()
        if message.get("type") != "event.created":
            return

        payload = message.get("payload") or {}
        event = payload.get("event") if isinstance(payload, dict) else None
        if not isinstance(event, dict):
            return

        tag = event.get("stressTag")
        publish_mono = event.get("_publishMono")
        if tag and isinstance(publish_mono, (int, float)):
            latency_ms = (received_at - float(publish_mono)) * 1000
            self.latencies_ms.append(latency_ms)
            self.received_tags.add(str(tag))


def _memory_mb() -> float:
    if HAS_PSUTIL:
        return psutil.Process().memory_info().rss / (1024 * 1024)
    import resource

    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Linux: KB, macOS: bytes
    if sys.platform == "darwin":
        return usage / (1024 * 1024)
    return usage / 1024


def _cpu_percent_sample(seconds: float = 0.15) -> float:
    if not HAS_PSUTIL:
        return 0.0
    try:
        return psutil.Process().cpu_percent(interval=seconds)
    except (PermissionError, SystemError, OSError):
        return 0.0


def _latency_stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {
            "min": 0.0,
            "avg": 0.0,
            "p50": 0.0,
            "p95": 0.0,
            "p99": 0.0,
            "max": 0.0,
        }

    ordered = sorted(values)

    def percentile(p: float) -> float:
        index = int(round((p / 100) * (len(ordered) - 1)))
        return ordered[max(0, min(index, len(ordered) - 1))]

    return {
        "min": ordered[0],
        "avg": statistics.mean(ordered),
        "p50": percentile(50),
        "p95": percentile(95),
        "p99": percentile(99),
        "max": ordered[-1],
    }


async def _wait_for_receipts(
    recorder: RecordingWebSocket,
    expected: int,
    *,
    timeout_sec: float,
) -> None:
    deadline = time.perf_counter() + timeout_sec
    while len(recorder.received_tags) < expected and time.perf_counter() < deadline:
        await asyncio.sleep(0.005)


async def run_pipeline_scenario(event_count: int) -> ScenarioResult:
    from app.core.event_bus import get_event_bus
    from app.core.event_bus.event_types import EVENT_CREATED
    from app.services.event_stream_service import event_stream_service
    from app.ws.connection_manager import events_manager

    loop = asyncio.get_running_loop()
    event_stream_service.set_app_loop(loop)
    event_stream_service.register()

    recorder = RecordingWebSocket()
    events_manager.active_connections = [recorder]

    errors: list[str] = []
    gc.collect()
    memory_before = _memory_mb()
    cpu_samples: list[float] = []

    started = time.perf_counter()
    bus = get_event_bus()

    for index in range(event_count):
        tag = f"stress-{event_count}-{index}"
        publish_mono = time.perf_counter()
        recorder.register_publish(tag, publish_mono)
        bus.publish(
            EVENT_CREATED,
            {
                "topic": EVENT_CREATED,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {
                    "event": {
                        "id": f"STRESS-{event_count}-{index:06d}",
                        "eventType": "UNIFORM_VIOLATION",
                        "stressTag": tag,
                        "_publishMono": publish_mono,
                    }
                },
            },
        )
        if index % 250 == 0:
            cpu_samples.append(_cpu_percent_sample(0.01))

    timeout = max(30.0, event_count / 200)
    await _wait_for_receipts(recorder, event_count, timeout_sec=timeout)

    duration = time.perf_counter() - started
    memory_after = _memory_mb()
    cpu_samples.append(_cpu_percent_sample(0.1))

    stats = _latency_stats(recorder.latencies_ms)
    if len(recorder.received_tags) < event_count:
        errors.append(
            f"Chỉ nhận {len(recorder.received_tags)}/{event_count} event qua WebSocket trong {timeout:.1f}s"
        )

    events_manager.active_connections = []

    return ScenarioResult(
        event_count=event_count,
        events_received=len(recorder.received_tags),
        duration_sec=round(duration, 4),
        events_per_sec=round(event_count / duration, 2) if duration else 0.0,
        latency_min_ms=round(stats["min"], 3),
        latency_avg_ms=round(stats["avg"], 3),
        latency_p50_ms=round(stats["p50"], 3),
        latency_p95_ms=round(stats["p95"], 3),
        latency_p99_ms=round(stats["p99"], 3),
        latency_max_ms=round(stats["max"], 3),
        memory_before_mb=round(memory_before, 2),
        memory_after_mb=round(memory_after, 2),
        memory_delta_mb=round(memory_after - memory_before, 2),
        cpu_percent_avg=round(statistics.mean(cpu_samples) if cpu_samples else 0.0, 2),
        errors=errors,
    )


async def run_live_scenario(event_count: int, api_url: str, token: str | None) -> ScenarioResult:
    import httpx

    ws_base = api_url.replace("https://", "wss://").replace("http://", "ws://").rstrip("/")
    ws_url = f"{ws_base}/ws/events"

    latencies_ms: list[float] = []
    received = 0
    errors: list[str] = []
    cpu_samples: list[float] = []

    memory_before = _memory_mb()
    if HAS_PSUTIL:
        try:
            server_proc = next(
                (p for p in psutil.process_iter(["name", "cmdline"]) if "uvicorn" in " ".join(p.info.get("cmdline") or [])),
                None,
            )
        except Exception:
            server_proc = None
    else:
        server_proc = None

    started = time.perf_counter()

    try:
        import websockets
    except ImportError as exc:
        raise RuntimeError("Live mode requires websockets (install uvicorn[standard])") from exc

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    async def listen(ws):
        nonlocal received
        async for raw in ws:
            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if message.get("type") != "event.created":
                continue
            payload = message.get("payload") or {}
            event = payload.get("event") if isinstance(payload, dict) else None
            if not isinstance(event, dict):
                continue
            tag = event.get("stressTag")
            publish_mono = event.get("_publishMono")
            if tag and isinstance(publish_mono, (int, float)):
                latencies_ms.append((time.perf_counter() - float(publish_mono)) * 1000)
                received += 1

    async with websockets.connect(ws_url) as ws:
        listener = asyncio.create_task(listen(ws))
        await asyncio.sleep(0.2)

        async with httpx.AsyncClient(base_url=api_url, timeout=120.0, headers=headers) as client:
            batch_size = 200
            published = 0
            while published < event_count:
                chunk = min(batch_size, event_count - published)
                batch = []
                for index in range(chunk):
                    global_index = published + index
                    tag = f"live-{event_count}-{global_index}"
                    publish_mono = time.perf_counter()
                    batch.append(
                        {
                            "id": f"LIVE-STRESS-{global_index:06d}",
                            "eventType": "UNIFORM_VIOLATION",
                            "stressTag": tag,
                            "_publishMono": publish_mono,
                        }
                    )
                response = await client.post("/api/stress/publish", json=batch)
                if response.status_code >= 400:
                    errors.append(f"Batch publish failed: HTTP {response.status_code} {response.text[:120]}")
                    break
                published += chunk
                if server_proc:
                    cpu_samples.append(server_proc.cpu_percent(interval=0.01))
                else:
                    cpu_samples.append(_cpu_percent_sample(0.01))

        timeout = max(60.0, event_count / 100)
        deadline = time.perf_counter() + timeout
        while received < event_count and time.perf_counter() < deadline:
            await asyncio.sleep(0.05)

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass

    duration = time.perf_counter() - started
    memory_after = _memory_mb()
    stats = _latency_stats(latencies_ms)

    if received < event_count:
        errors.append(f"Live mode received {received}/{event_count} events")

    return ScenarioResult(
        event_count=event_count,
        events_received=received,
        duration_sec=round(duration, 4),
        events_per_sec=round(event_count / duration, 2) if duration else 0.0,
        latency_min_ms=round(stats["min"], 3),
        latency_avg_ms=round(stats["avg"], 3),
        latency_p50_ms=round(stats["p50"], 3),
        latency_p95_ms=round(stats["p95"], 3),
        latency_p99_ms=round(stats["p99"], 3),
        latency_max_ms=round(stats["max"], 3),
        memory_before_mb=round(memory_before, 2),
        memory_after_mb=round(memory_after, 2),
        memory_delta_mb=round(memory_after - memory_before, 2),
        cpu_percent_avg=round(statistics.mean(cpu_samples) if cpu_samples else 0.0, 2),
        errors=errors,
    )


def _login(api_url: str, email: str, password: str) -> str | None:
    import httpx

    try:
        response = httpx.post(
            f"{api_url.rstrip('/')}/api/auth/login",
            json={"email": email, "password": password},
            timeout=15.0,
        )
        if response.status_code >= 400:
            return None
        return response.json().get("access_token")
    except Exception:
        return None


def render_report(results: list[ScenarioResult], *, mode: str, generated_at: str) -> str:
    lines = [
        "# WebSocket Stress Test Report",
        "",
        f"**Generated:** {generated_at}  ",
        f"**Mode:** `{mode}`  ",
        f"**Path:** EventBus → EventStreamService → `/ws/events`",
        "",
        "## Summary",
        "",
        "| Events | Received | Duration (s) | Throughput (evt/s) | Latency avg (ms) | Latency p95 (ms) | Latency p99 (ms) | Memory Δ (MB) | CPU avg (%) |",
        "|--------|----------|--------------|--------------------|------------------|------------------|------------------|---------------|-------------|",
    ]

    for item in results:
        lines.append(
            f"| {item.event_count} | {item.events_received} | {item.duration_sec} | "
            f"{item.events_per_sec} | {item.latency_avg_ms} | {item.latency_p95_ms} | "
            f"{item.latency_p99_ms} | {item.memory_delta_mb} | {item.cpu_percent_avg} |"
        )

    lines.extend(
        [
            "",
            "## Latency detail",
            "",
        ]
    )

    for item in results:
        lines.extend(
            [
                f"### {item.event_count} events",
                "",
                "| Metric | ms |",
                "|--------|-----|",
                f"| min | {item.latency_min_ms} |",
                f"| avg | {item.latency_avg_ms} |",
                f"| p50 | {item.latency_p50_ms} |",
                f"| p95 | {item.latency_p95_ms} |",
                f"| p99 | {item.latency_p99_ms} |",
                f"| max | {item.latency_max_ms} |",
                "",
                f"- Memory: {item.memory_before_mb} → {item.memory_after_mb} MB (Δ {item.memory_delta_mb} MB)",
                f"- CPU avg (process): {item.cpu_percent_avg}%",
                "",
            ]
        )
        if item.errors:
            lines.append("**Warnings:**")
            for error in item.errors:
                lines.append(f"- {error}")
            lines.append("")

    lines.extend(
        [
            "## Methodology",
            "",
            "1. Publish `event.created` messages through in-process EventBus.",
            "2. EventStreamService forwards to WebSocket broadcast handler.",
            "3. Latency = WebSocket `send_json` receive time − publish monotonic time.",
            "4. Memory/CPU measured on stress test process"
            + (" via psutil" if HAS_PSUTIL else " (install psutil for accurate CPU)"),
            ".",
            "",
            "## How to run",
            "",
            "```bash",
            "cd backend",
            "python scripts/websocket_stress_test.py",
            "python scripts/websocket_stress_test.py --live --api-url http://127.0.0.1:8000",
            "```",
            "",
            "## Interpretation",
            "",
            "| Latency p95 | Assessment |",
            "|-------------|------------|",
            "| < 5 ms | Excellent (in-process) |",
            "| 5–20 ms | Good |",
            "| 20–100 ms | Acceptable under load |",
            "| > 100 ms | Investigate WS fan-out / CPU saturation |",
            "",
            "| Memory Δ | Assessment |",
            "|----------|------------|",
            "| < 50 MB per 10k events | Stable |",
            "| 50–200 MB | Monitor for leak over time |",
            "| > 200 MB | Review connection cleanup |",
            "",
            "## Conclusions",
            "",
        ]
    )

    all_ok = all(r.events_received == r.event_count for r in results)
    max_p95 = max((r.latency_p95_ms for r in results), default=0.0)
    max_mem = max((r.memory_delta_mb for r in results), default=0.0)

    if all_ok and max_p95 < 20:
        lines.append(
            f"- All scenarios delivered 100% of events. Max p95 latency {max_p95:.2f} ms — excellent for in-process pipeline."
        )
    elif all_ok:
        lines.append(
            f"- All scenarios delivered 100% of events. Max p95 latency {max_p95:.2f} ms — review if live mode exceeds 100 ms."
        )
    else:
        lines.append("- Some scenarios lost events — investigate EventBus backpressure or WS disconnects.")

    lines.append(
        f"- Peak memory delta across scenarios: {max_mem:.2f} MB"
        + (" — stable." if max_mem < 50 else " — monitor under sustained load.")
    )
    if mode == "pipeline":
        lines.append(
            "- Pipeline mode validates EventBus → EventStreamService → WS handler without HTTP/DB overhead."
        )
        lines.append(
            "- For end-to-end numbers, run with `STRESS_TEST=true` and `--live` against a running server."
        )
    lines.append("")

    return "\n".join(lines)


async def main_async(args: argparse.Namespace) -> list[ScenarioResult]:
    results: list[ScenarioResult] = []
    token = None
    if args.live:
        token = _login(args.api_url, args.email, args.password)

    for count in EVENT_COUNTS:
        print(f"Running scenario: {count} events ({args.mode})...")
        if args.live:
            result = await run_live_scenario(count, args.api_url, token)
        else:
            result = await run_pipeline_scenario(count)
        results.append(result)
        print(
            f"  received={result.events_received}/{count} "
            f"p95={result.latency_p95_ms}ms memΔ={result.memory_delta_mb}MB"
        )
        gc.collect()
        await asyncio.sleep(0.5)

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="AMS WebSocket stress test")
    parser.add_argument("--live", action="store_true", help="Test against running AMS server")
    parser.add_argument("--api-url", default="http://127.0.0.1:8000")
    parser.add_argument("--email", default="admin@ams.local")
    parser.add_argument("--password", default="admin123")
    parser.add_argument(
        "--output",
        default=str(BACKEND_ROOT.parent / "WEBSOCKET_STRESS_REPORT.md"),
        help="Report output path",
    )
    args = parser.parse_args()
    args.mode = "live" if args.live else "pipeline"

    results = asyncio.run(main_async(args))
    generated_at = datetime.now(timezone.utc).isoformat()
    report = render_report(results, mode=args.mode, generated_at=generated_at)

    output_path = Path(args.output)
    output_path.write_text(report, encoding="utf-8")
    print(f"\nReport written: {output_path}")


if __name__ == "__main__":
    main()
