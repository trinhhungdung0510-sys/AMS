from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.core.observation_schema import DEFAULT_SCHEMA_VERSION


def normalize_bbox_xyxy(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    frame_width: int,
    frame_height: int,
) -> dict[str, float]:
    if frame_width <= 0 or frame_height <= 0:
        raise ValueError("frame dimensions must be positive")

    width_px = max(0.0, x2 - x1)
    height_px = max(0.0, y2 - y1)
    return {
        "x": round(max(0.0, min(1.0, x1 / frame_width)), 6),
        "y": round(max(0.0, min(1.0, y1 / frame_height)), 6),
        "width": round(max(0.0, min(1.0, width_px / frame_width)), 6),
        "height": round(max(0.0, min(1.0, height_px / frame_height)), 6),
    }


def build_observation_object(
    *,
    track_id: str,
    object_class: str,
    confidence: float,
    bbox: dict[str, float],
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "trackId": track_id,
        "class": object_class,
        "confidence": round(float(confidence), 4),
        "bbox": bbox,
        "attributes": attributes or {},
    }


def build_observation_payload(
    *,
    camera_id: str,
    objects: list[dict[str, Any]],
    frame_width: int,
    frame_height: int,
    source: str = "YOLO",
    timestamp: str | None = None,
    schema_version: str = DEFAULT_SCHEMA_VERSION,
) -> dict[str, Any]:
    return {
        "schemaVersion": schema_version,
        "cameraId": camera_id,
        "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
        "source": source,
        "frameWidth": frame_width,
        "frameHeight": frame_height,
        "objects": objects,
    }
