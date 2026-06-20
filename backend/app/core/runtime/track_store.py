from __future__ import annotations

from typing import Any, Optional


def track_key(camera_id: str, track_id: str) -> str:
    return f"{camera_id}:{track_id}"


class TrackStore:
    def __init__(self) -> None:
        self._tracks: dict[str, dict[str, Any]] = {}

    def upsert_track(
        self,
        *,
        camera_id: str,
        track_id: str,
        object_class: str,
        timestamp: str,
        current_zone_id: Optional[str] = None,
        current_sub_zone_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> tuple[dict[str, Any], bool, Optional[dict[str, Any]]]:
        key = track_key(camera_id, track_id)
        existing = self._tracks.get(key)
        metadata = metadata or {}

        if not existing:
            track = {
                "trackId": track_id,
                "cameraId": camera_id,
                "class": object_class,
                "firstSeenAt": timestamp,
                "lastSeenAt": timestamp,
                "currentZoneId": current_zone_id,
                "currentSubZoneId": current_sub_zone_id,
                "metadata": dict(metadata),
            }
            self._tracks[key] = track
            return track, True, None

        previous = dict(existing)
        existing["lastSeenAt"] = timestamp
        existing["class"] = object_class or existing.get("class")
        existing["currentZoneId"] = current_zone_id
        existing["currentSubZoneId"] = current_sub_zone_id
        existing["metadata"] = {**existing.get("metadata", {}), **metadata}
        self._tracks[key] = existing
        return existing, False, previous

    def get_track(self, camera_id: str, track_id: str) -> Optional[dict[str, Any]]:
        return self._tracks.get(track_key(camera_id, track_id))

    def remove_track(self, camera_id: str, track_id: str) -> bool:
        return self._tracks.pop(track_key(camera_id, track_id), None) is not None

    def get_tracks_by_camera(self, camera_id: str) -> list[dict[str, Any]]:
        prefix = f"{camera_id}:"
        return [track for key, track in self._tracks.items() if key.startswith(prefix)]

    def clear(self) -> None:
        self._tracks.clear()


_track_store: TrackStore | None = None


def get_track_store() -> TrackStore:
    global _track_store
    if _track_store is None:
        _track_store = TrackStore()
    return _track_store
