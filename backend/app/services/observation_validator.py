from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from app.core.observation_schema import DEFAULT_SCHEMA_VERSION, migrate_observation_payload, normalize_schema_version
from app.models.observation import OBJECT_CLASSES, OBSERVATION_SOURCES
from app.schemas.observation import BboxNormalized, ObservationCreate, ObservationObject


class ObservationValidator:
    """Validates observation payloads before persistence or replay."""

    def validate(self, payload: dict[str, Any]) -> ObservationCreate:
        migrated = migrate_observation_payload(payload)
        version = normalize_schema_version(
            migrated.get("schemaVersion") or migrated.get("schema_version")
        )

        for index, obj in enumerate(migrated.get("objects") or []):
            self._validate_object(obj, index)

        try:
            create_payload = ObservationCreate(
                cameraId=migrated.get("cameraId") or migrated.get("camera_id"),
                timestamp=migrated["timestamp"],
                source=migrated["source"],
                frameWidth=migrated.get("frameWidth") or migrated.get("frame_width"),
                frameHeight=migrated.get("frameHeight") or migrated.get("frame_height"),
                objects=[ObservationObject(**self._normalize_object(obj)) for obj in migrated.get("objects") or []],
                schemaVersion=version,
            )
        except ValidationError as exc:
            raise ValueError(str(exc)) from exc

        return create_payload

    def _validate_object(self, obj: dict[str, Any], index: int) -> None:
        track_id = obj.get("trackId") or obj.get("track_id")
        if not track_id or not str(track_id).strip():
            raise ValueError(f"objects[{index}].trackId is required")

        object_class = obj.get("class") or obj.get("object_class")
        if not object_class:
            raise ValueError(f"objects[{index}].class is required")
        normalized_class = str(object_class).strip().lower()
        if normalized_class not in {item.lower() for item in OBJECT_CLASSES}:
            raise ValueError(f"objects[{index}].class is invalid")

        confidence = obj.get("confidence")
        if confidence is None or not (0 <= float(confidence) <= 1):
            raise ValueError(f"objects[{index}].confidence must be between 0 and 1")

        bbox = obj.get("bbox")
        if not bbox:
            raise ValueError(f"objects[{index}].bbox is required")
        try:
            BboxNormalized(**bbox)
        except ValidationError as exc:
            raise ValueError(f"objects[{index}].bbox invalid: {exc}") from exc

    def _normalize_object(self, obj: dict[str, Any]) -> dict[str, Any]:
        return {
            "trackId": obj.get("trackId") or obj.get("track_id"),
            "class": obj.get("class") or obj.get("object_class"),
            "confidence": obj.get("confidence"),
            "bbox": obj.get("bbox"),
            "attributes": obj.get("attributes") or {},
        }


observation_validator = ObservationValidator()
