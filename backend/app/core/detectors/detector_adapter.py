from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from app.core.detectors.capabilities import (
    DETECTOR_STATUS_STOPPED,
    DetectorCapabilities,
    DetectorHealth,
)


ObservationCallback = Callable[[dict[str, Any]], None]


class DetectorAdapter(ABC):
    """Detector adapter v2 — lifecycle + capabilities + observation emission."""

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def source(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def health(self) -> DetectorHealth:
        raise NotImplementedError

    @abstractmethod
    def get_capabilities(self) -> DetectorCapabilities:
        raise NotImplementedError

    @abstractmethod
    def on_observation(self, callback: ObservationCallback) -> None:
        """Register callback invoked when detector emits an observation payload."""
        raise NotImplementedError

    def detect(self, context: dict[str, Any]) -> dict[str, Any]:
        """Optional one-shot detect for mock/testing."""
        raise NotImplementedError(f"{self.name} does not implement detect()")

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "source": self.source,
            "health": self.health().to_dict(),
            "capabilities": self.get_capabilities().to_dict(),
        }


class BaseDetectorAdapter(DetectorAdapter):
    def __init__(self, name: str, source: str, capabilities: DetectorCapabilities) -> None:
        self._name = name
        self._source = source
        self._capabilities = capabilities
        self._callback: Optional[ObservationCallback] = None
        self._health = DetectorHealth(status=DETECTOR_STATUS_STOPPED)

    @property
    def name(self) -> str:
        return self._name

    @property
    def source(self) -> str:
        return self._source

    def on_observation(self, callback: ObservationCallback) -> None:
        self._callback = callback

    def get_capabilities(self) -> DetectorCapabilities:
        return self._capabilities

    def health(self) -> DetectorHealth:
        return self._health

    def _emit_observation(self, payload: dict[str, Any]) -> None:
        if self._callback:
            self._callback(payload)
        self._health.observations_emitted += 1
