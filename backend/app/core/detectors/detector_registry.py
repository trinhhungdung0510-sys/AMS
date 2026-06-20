from __future__ import annotations

import logging
from typing import Optional

from app.core.detectors.detector_adapter import DetectorAdapter

logger = logging.getLogger(__name__)


class DetectorRegistry:
    def __init__(self) -> None:
        self._detectors: dict[str, DetectorAdapter] = {}

    def register(self, detector: DetectorAdapter) -> None:
        if detector.name in self._detectors:
            logger.warning("Replacing detector registration: %s", detector.name)
        self._detectors[detector.name] = detector
        logger.info("Registered detector: %s", detector.name)

    def unregister(self, detector_name: str) -> bool:
        if detector_name not in self._detectors:
            return False
        del self._detectors[detector_name]
        logger.info("Unregistered detector: %s", detector_name)
        return True

    def get(self, detector_name: str) -> Optional[DetectorAdapter]:
        return self._detectors.get(detector_name)

    def list(self) -> list[DetectorAdapter]:
        return list(self._detectors.values())

    def list_dicts(self) -> list[dict]:
        return [detector.to_dict() for detector in self.list()]


_registry: DetectorRegistry | None = None


def get_detector_registry() -> DetectorRegistry:
    global _registry
    if _registry is None:
        _registry = DetectorRegistry()
    return _registry
