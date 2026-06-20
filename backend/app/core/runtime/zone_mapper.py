from __future__ import annotations

from typing import Any

from app.utils.zone_geometry import bbox_center, point_in_polygon, resolve_normalized_points


def map_observation_to_zones(observation: dict[str, Any], zones: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mappings: list[dict[str, Any]] = []
    frame_width = observation.get("frame_width") or observation.get("frameWidth")
    frame_height = observation.get("frame_height") or observation.get("frameHeight")

    for obj in observation.get("objects") or []:
        track_id = obj.get("trackId") or obj.get("track_id")
        center = bbox_center(obj["bbox"])
        zones_matched: list[str] = []
        subzones_matched: list[str] = []

        for zone in zones:
            polygon = resolve_normalized_points(
                zone.get("points") or [],
                points_format=zone.get("points_format"),
                reference_width=zone.get("reference_width"),
                reference_height=zone.get("reference_height"),
                fallback_width=frame_width,
                fallback_height=frame_height,
            )
            if not point_in_polygon(center, polygon):
                continue

            if zone.get("parent_zone_id"):
                subzones_matched.append(zone["id"])
            else:
                zones_matched.append(zone["id"])

        mappings.append(
            {
                "objectId": track_id,
                "zones": zones_matched,
                "subzones": subzones_matched,
            }
        )

    return mappings


def object_in_zone(mapping: dict[str, Any], zone_id: str) -> bool:
    return zone_id in mapping.get("zones", []) or zone_id in mapping.get("subzones", [])
