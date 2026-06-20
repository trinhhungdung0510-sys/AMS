#!/usr/bin/env python3
"""Simulate observation throughput for 10 / 50 / 100 cameras."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from app.core.event_bus.event_bus import InMemoryEventBus
from app.core.event_bus.event_types import OBSERVATION_CREATED
from app.services.observation_validator import observation_validator
from app.services.pipeline_subscribers import register_pipeline_subscribers
from app.services.runtime_metrics_service import register_metrics_subscribers


def load_fixture(name: str) -> dict:
    path = BACKEND_ROOT.parent / "fixtures" / "observations" / name
    import json

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def simulate(camera_count: int, fixture_name: str, iterations: int = 1) -> dict:
    bus = InMemoryEventBus()
    import app.core.event_bus.event_bus as event_bus_module

    event_bus_module._event_bus = bus
    register_pipeline_subscribers()
    register_metrics_subscribers()

    template = load_fixture(fixture_name)
    start = time.perf_counter()

    for i in range(iterations):
        for cam_index in range(camera_count):
            payload = {
                **template,
                "cameraId": f"CAM-LOAD-{cam_index:03d}",
                "timestamp": f"2026-06-23T10:00:{cam_index % 60:02d}+00:00",
            }
            validated = observation_validator.validate(payload)
            bus.publish(
                OBSERVATION_CREATED,
                {
                    "topic": OBSERVATION_CREATED,
                    "data": {
                        "observation": {
                            **validated.model_dump(by_alias=False),
                            "camera_id": f"CAM-LOAD-{cam_index:03d}",
                        }
                    },
                },
            )

    elapsed = time.perf_counter() - start
    total = camera_count * iterations
    return {
        "cameras": camera_count,
        "iterations": iterations,
        "observations": total,
        "elapsedSec": round(elapsed, 4),
        "observationsPerSec": round(total / elapsed, 2) if elapsed else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="AMS observation load test")
    parser.add_argument("--fixture", default="person_enter.json")
    parser.add_argument("--iterations", type=int, default=1)
    args = parser.parse_args()

    for count in (10, 50, 100):
        result = simulate(count, args.fixture, args.iterations)
        print(result)


if __name__ == "__main__":
    main()
