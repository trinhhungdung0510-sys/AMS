from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.event_bus import get_event_bus
from app.core.event_bus import event_types as topics
from app.models import Event, Observation
from app.ws.connection_manager import events_manager

logger = logging.getLogger(__name__)


@dataclass
class RuntimeMetrics:
    observations_per_sec: float = 0.0
    events_per_sec: float = 0.0
    connected_ws_clients: int = 0
    open_events: int = 0
    detector_count: int = 0
    observation_total: int = 0
    event_total: int = 0
    window_seconds: float = 60.0
    _observation_window: list[float] = field(default_factory=list)
    _event_window: list[float] = field(default_factory=list)

    def record_observation(self) -> None:
        now = time.time()
        self.observation_total += 1
        self._observation_window.append(now)
        self._trim(now)

    def record_event(self) -> None:
        now = time.time()
        self.event_total += 1
        self._event_window.append(now)
        self._trim(now)

    def _trim(self, now: float) -> None:
        cutoff = now - self.window_seconds
        self._observation_window = [item for item in self._observation_window if item >= cutoff]
        self._event_window = [item for item in self._event_window if item >= cutoff]
        self.observations_per_sec = len(self._observation_window) / self.window_seconds
        self.events_per_sec = len(self._event_window) / self.window_seconds

    def refresh_runtime(self, db: Session, detector_count: int) -> dict[str, Any]:
        now = time.time()
        self._trim(now)
        self.connected_ws_clients = len(events_manager.active_connections)
        self.detector_count = detector_count
        self.open_events = db.scalar(
            select(func.count()).select_from(Event).where(Event.status == "OPEN")
        ) or 0
        return self.to_dict()

    def to_dict(self) -> dict[str, Any]:
        return {
            "observationsPerSec": round(self.observations_per_sec, 3),
            "eventsPerSec": round(self.events_per_sec, 3),
            "connectedWsClients": self.connected_ws_clients,
            "openEvents": self.open_events,
            "detectorCount": self.detector_count,
            "observationTotal": self.observation_total,
            "eventTotal": self.event_total,
            "windowSeconds": self.window_seconds,
        }


runtime_metrics = RuntimeMetrics()


def register_metrics_subscribers() -> None:
    bus = get_event_bus()

    def on_observation(_message: dict[str, Any]) -> None:
        runtime_metrics.record_observation()

    def on_event(_message: dict[str, Any]) -> None:
        runtime_metrics.record_event()

    bus.subscribe(topics.OBSERVATION_CREATED, on_observation)
    bus.subscribe(topics.EVENT_CREATED, on_event)
    logger.info("Runtime metrics subscribers registered")
