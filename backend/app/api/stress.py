from __future__ import annotations

import time
from datetime import datetime, timezone

from fastapi import APIRouter, Body, HTTPException, status

from app.core.config import get_settings
from app.core.event_bus import get_event_bus
from app.core.event_bus.event_types import EVENT_CREATED

router = APIRouter(prefix="/stress", tags=["stress"])


def _ensure_stress_enabled() -> None:
    if not get_settings().stress_test_enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Stress test API disabled. Set STRESS_TEST=true to enable.",
        )


@router.post("/publish")
def publish_stress_events(events: list[dict] = Body(...)) -> dict:
    _ensure_stress_enabled()
    if len(events) > 500:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Max 500 events per request")

    bus = get_event_bus()
    now = datetime.now(timezone.utc).isoformat()
    for event in events:
        publish_mono = event.get("_publishMono", time.perf_counter())
        bus.publish(
            EVENT_CREATED,
            {
                "topic": EVENT_CREATED,
                "timestamp": now,
                "data": {"event": {**event, "_publishMono": publish_mono}},
            },
        )

    return {"published": len(events)}
