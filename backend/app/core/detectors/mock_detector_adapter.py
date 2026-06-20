from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.core.detectors.capabilities import (
    DETECTOR_STATUS_FAILED,
    DETECTOR_STATUS_RUNNING,
    DETECTOR_STATUS_STARTING,
    DETECTOR_STATUS_STOPPED,
    DetectorCapabilities,
)
from app.core.detectors.detector_adapter import BaseDetectorAdapter
from app.core.event_bus import get_event_bus
from app.core.event_bus import event_types as topics
from app.core.observation_schema import DEFAULT_SCHEMA_VERSION
from app.services.observation_service import utc_now_iso

SCENARIOS: dict[str, dict[str, Any]] = {
    "one_person": {
        "objects": [
            {
                "trackId": "T-001",
                "class": "person",
                "confidence": 0.94,
                "bbox": {"x": 0.35, "y": 0.2, "width": 0.12, "height": 0.45},
                "attributes": {"helmet": True, "mask": True, "coverall": True},
            }
        ]
    },
    "three_persons": {
        "objects": [
            {
                "trackId": "T-101",
                "class": "person",
                "confidence": 0.91,
                "bbox": {"x": 0.1, "y": 0.25, "width": 0.1, "height": 0.4},
                "attributes": {"helmet": True, "mask": False, "coverall": True},
            },
            {
                "trackId": "T-102",
                "class": "person",
                "confidence": 0.88,
                "bbox": {"x": 0.35, "y": 0.22, "width": 0.11, "height": 0.42},
                "attributes": {"helmet": True, "mask": True, "coverall": True},
            },
            {
                "trackId": "T-103",
                "class": "person",
                "confidence": 0.86,
                "bbox": {"x": 0.62, "y": 0.28, "width": 0.1, "height": 0.38},
                "attributes": {"helmet": False, "mask": True, "coverall": True},
            },
        ]
    },
}


def _publish_detector_event(topic: str, detector_name: str, **extra: Any) -> None:
    get_event_bus().publish(
        topic,
        {
            "topic": topic,
            "timestamp": utc_now_iso(),
            "data": {"detectorName": detector_name, **extra},
        },
    )


class MockDetectorAdapter(BaseDetectorAdapter):
    def __init__(self) -> None:
        super().__init__(
            name="mock-detector-v1",
            source="MOCK",
            capabilities=DetectorCapabilities(
                person_detection=True,
                animal_detection=True,
                ppe_detection=True,
                tracking=True,
            ),
        )

    def start(self) -> None:
        self._health.status = DETECTOR_STATUS_STARTING
        self._health.message = "Starting mock detector"
        _publish_detector_event(topics.DETECTOR_STARTED, self.name)
        self._health.status = DETECTOR_STATUS_RUNNING
        self._health.started_at = utc_now_iso()
        self._health.message = "Mock detector running"

    def stop(self) -> None:
        self._health.status = DETECTOR_STATUS_STOPPED
        self._health.stopped_at = utc_now_iso()
        self._health.message = "Mock detector stopped"
        _publish_detector_event(topics.DETECTOR_STOPPED, self.name)

    def detect(self, context: dict[str, Any]) -> dict[str, Any]:
        scenario_key = context.get("scenarioKey") or context.get("scenario_key") or "one_person"
        scenario = SCENARIOS.get(scenario_key)
        if not scenario and context.get("objects"):
            scenario = {"objects": context["objects"]}
        if not scenario:
            raise ValueError(f"Unknown mock scenario: {scenario_key}")

        payload = {
            "cameraId": context["cameraId"],
            "timestamp": context.get("timestamp") or datetime.now(timezone.utc).isoformat(),
            "source": self.source,
            "schemaVersion": context.get("schemaVersion") or DEFAULT_SCHEMA_VERSION,
            "frameWidth": context.get("frameWidth") or 1920,
            "frameHeight": context.get("frameHeight") or 1080,
            "objects": [dict(item) for item in scenario["objects"]],
        }
        self._emit_observation(payload)
        return payload
