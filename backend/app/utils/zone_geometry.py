"""Geometry helpers for camera zones — pixel ↔ normalized coordinates."""

from __future__ import annotations

from typing import Optional

POINTS_FORMAT_PIXEL = "pixel"
POINTS_FORMAT_NORMALIZED = "normalized"


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def normalize_point(point: dict, reference_width: float, reference_height: float) -> dict:
    if not reference_width or not reference_height:
        return {"x": 0.0, "y": 0.0}
    return {
        "x": clamp(float(point["x"]) / reference_width),
        "y": clamp(float(point["y"]) / reference_height),
    }


def denormalize_point(point: dict, reference_width: float, reference_height: float) -> dict:
    return {
        "x": float(point["x"]) * reference_width,
        "y": float(point["y"]) * reference_height,
    }


def scale_polygon_to_normalized(
    points: list[dict],
    reference_width: float,
    reference_height: float,
) -> list[dict]:
    return [normalize_point(point, reference_width, reference_height) for point in points]


def is_legacy_pixel_zone(
    points: list[dict],
    points_format: Optional[str] = None,
) -> bool:
    if points_format == POINTS_FORMAT_NORMALIZED:
        return False
    if points_format == POINTS_FORMAT_PIXEL:
        return True
    return any(float(point.get("x", 0)) > 1.0 or float(point.get("y", 0)) > 1.0 for point in points)


def resolve_normalized_points(
    points: list[dict],
    *,
    points_format: Optional[str] = None,
    reference_width: Optional[int] = None,
    reference_height: Optional[int] = None,
    fallback_width: Optional[int] = None,
    fallback_height: Optional[int] = None,
) -> list[dict]:
    if not is_legacy_pixel_zone(points, points_format):
        return [{"x": float(point["x"]), "y": float(point["y"])} for point in points]

    ref_w = reference_width or fallback_width
    ref_h = reference_height or fallback_height
    if not ref_w or not ref_h:
        return [{"x": float(point["x"]), "y": float(point["y"])} for point in points]

    return scale_polygon_to_normalized(points, float(ref_w), float(ref_h))
