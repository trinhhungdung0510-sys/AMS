from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DetectorCapabilities:
    person_detection: bool = False
    animal_detection: bool = False
    ppe_detection: bool = False
    tracking: bool = False

    def to_dict(self) -> dict[str, bool]:
        return {
            "person_detection": self.person_detection,
            "animal_detection": self.animal_detection,
            "ppe_detection": self.ppe_detection,
            "tracking": self.tracking,
        }


DETECTOR_STATUS_STARTING = "STARTING"
DETECTOR_STATUS_RUNNING = "RUNNING"
DETECTOR_STATUS_DEGRADED = "DEGRADED"
DETECTOR_STATUS_STOPPED = "STOPPED"
DETECTOR_STATUS_FAILED = "FAILED"

DETECTOR_STATUSES = {
    DETECTOR_STATUS_STARTING,
    DETECTOR_STATUS_RUNNING,
    DETECTOR_STATUS_DEGRADED,
    DETECTOR_STATUS_STOPPED,
    DETECTOR_STATUS_FAILED,
}


@dataclass
class DetectorHealth:
    status: str = DETECTOR_STATUS_STOPPED
    message: str = ""
    last_error: str | None = None
    started_at: str | None = None
    stopped_at: str | None = None
    observations_emitted: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "message": self.message,
            "lastError": self.last_error,
            "startedAt": self.started_at,
            "stoppedAt": self.stopped_at,
            "observationsEmitted": self.observations_emitted,
        }
