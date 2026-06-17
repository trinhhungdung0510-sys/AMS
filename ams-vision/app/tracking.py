import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests

from app.detector import Detection


@dataclass
class ObjectTrack:
    track_id: int
    camera_id: str
    object_type: str
    current_zone: str
    previous_zone: Optional[str]
    enter_time: str
    leave_time: Optional[str]
    bbox: tuple[int, int, int, int]
    confidence: float
    last_seen: str


class ZoneResolver:
    def __init__(self, backend_base_url: str, camera_id: str, refresh_seconds: int = 30) -> None:
        self.backend_base_url = backend_base_url.rstrip("/")
        self.camera_id = camera_id
        self.refresh_seconds = refresh_seconds
        self.zones: list[dict] = []
        self._last_refresh = 0.0

    def get_zone(self, detection: Detection) -> str:
        self._refresh_if_needed()
        x1, y1, x2, y2 = detection.bbox
        point = ((x1 + x2) / 2, (y1 + y2) / 2)
        for zone in self.zones:
            if self._point_in_polygon(point, zone["polygon_points"]):
                return zone["zone_type"]
        return "unknown"

    def _refresh_if_needed(self) -> None:
        now = time.time()
        if now - self._last_refresh < self.refresh_seconds and self.zones:
            return

        response = requests.get(f"{self.backend_base_url}/api/zones", timeout=5)
        response.raise_for_status()
        zones = response.json()
        self.zones = [
            zone
            for zone in zones
            if zone.get("camera_id") == self.camera_id and zone.get("active", True)
        ]
        self._last_refresh = now

    @staticmethod
    def _point_in_polygon(point: tuple[float, float], polygon: list[list[float]]) -> bool:
        x, y = point
        inside = False
        j = len(polygon) - 1
        for i, current in enumerate(polygon):
            xi, yi = current
            xj, yj = polygon[j]
            intersects = (yi > y) != (yj > y) and x < ((xj - xi) * (y - yi) / ((yj - yi) or 1e-9) + xi)
            if intersects:
                inside = not inside
            j = i
        return inside


class TrackingEngine:
    def __init__(self, backend_base_url: str, camera_id: str, history_path: str) -> None:
        self.camera_id = camera_id
        self.zone_resolver = ZoneResolver(backend_base_url, camera_id)
        self.history_path = Path(history_path)
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        self.active_tracks: dict[int, ObjectTrack] = {}
        self.track_history: list[dict] = self._load_history()
        self.latest_transitions: list[dict] = []
        self._next_local_track_id = 1000

    def update(self, detections: list[Detection]) -> list[ObjectTrack]:
        now = datetime.now(timezone.utc).isoformat()
        updated: list[ObjectTrack] = []
        seen_track_ids: set[int] = set()
        self.latest_transitions = []

        for detection in detections:
            track_id = detection.track_id or self._assign_local_track_id(detection)
            seen_track_ids.add(track_id)
            current_zone = self._resolve_zone(detection)
            existing = self.active_tracks.get(track_id)

            if existing is None:
                track = ObjectTrack(
                    track_id=track_id,
                    camera_id=self.camera_id,
                    object_type=detection.label,
                    current_zone=current_zone,
                    previous_zone=None,
                    enter_time=now,
                    leave_time=None,
                    bbox=detection.bbox,
                    confidence=detection.confidence,
                    last_seen=now,
                )
                self.active_tracks[track_id] = track
                self.track_history.append(asdict(track))
                updated.append(track)
                continue

            if existing.current_zone != current_zone:
                transition = {
                    "object_type": existing.object_type,
                    "track_id": existing.track_id,
                    "from_zone": existing.current_zone,
                    "to_zone": current_zone,
                    "timestamp": now,
                }
                self.latest_transitions.append(transition)
                existing.previous_zone = existing.current_zone
                existing.current_zone = current_zone
                existing.enter_time = now
                existing.leave_time = None

            existing.object_type = detection.label
            existing.bbox = detection.bbox
            existing.confidence = detection.confidence
            existing.last_seen = now
            updated.append(existing)

        for track_id, track in list(self.active_tracks.items()):
            if track_id not in seen_track_ids and track.leave_time is None:
                track.leave_time = now

        self._persist_history()
        return updated

    def list_tracks(self) -> list[dict]:
        merged = {item["track_id"]: item for item in self.track_history}
        for track in self.active_tracks.values():
            merged[track.track_id] = asdict(track)
        return sorted(merged.values(), key=lambda item: item["last_seen"], reverse=True)

    def _assign_local_track_id(self, detection: Detection) -> int:
        # Fallback for detections without ByteTrack IDs.
        self._next_local_track_id += 1
        return self._next_local_track_id

    def _resolve_zone(self, detection: Detection) -> str:
        try:
            return self.zone_resolver.get_zone(detection)
        except Exception:
            return "unknown"

    def _load_history(self) -> list[dict]:
        if not self.history_path.exists():
            return []
        try:
            return json.loads(self.history_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def _persist_history(self) -> None:
        history = self.list_tracks()
        self.history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
