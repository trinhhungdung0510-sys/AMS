from __future__ import annotations

import logging

from app.core.detectors import MockDetectorAdapter, get_detector_registry
from app.database.session import SessionLocal
from app.services.observation_service import create_observation
from app.services.observation_validator import observation_validator

logger = logging.getLogger(__name__)


def register_default_detectors() -> None:
    registry = get_detector_registry()
    mock = MockDetectorAdapter()

    def handle_observation(payload: dict) -> None:
        db = SessionLocal()
        try:
            validated = observation_validator.validate(payload)
            create_observation(db, validated)
        except Exception:
            logger.exception("Detector observation ingest failed")
        finally:
            db.close()

    mock.on_observation(handle_observation)
    registry.register(mock)
    mock.start()
    logger.info("Default detectors registered and started")


def shutdown_detectors() -> None:
    for detector in get_detector_registry().list():
        try:
            detector.stop()
        except Exception:
            logger.exception("Failed stopping detector %s", detector.name)
