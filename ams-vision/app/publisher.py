import requests
from typing import Optional


class EventPublisher:
    def __init__(self, backend_base_url: str) -> None:
        self.backend_base_url = backend_base_url.rstrip("/")

    def publish_detection(self, *, camera_id: str, category: str, priority: int = 8) -> dict:
        response = requests.post(
            f"{self.backend_base_url}/api/tasks/simulate-alert",
            params={
                "camera_id": camera_id,
                "category": category,
                "priority": priority,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def publish_crossing(
        self,
        *,
        track_id: int,
        camera_id: str,
        zone_id: str,
        timestamp: str,
        object_type: Optional[str] = None,
    ) -> Optional[dict]:
        payload = {
            "track_id": track_id,
            "camera_id": camera_id,
            "zone_id": zone_id,
            "timestamp": timestamp,
        }
        if object_type:
            payload["object_type"] = object_type
        response = requests.post(
            f"{self.backend_base_url}/api/transitions/cross",
            json=payload,
            timeout=10,
        )
        if response.status_code == 204:
            return None
        response.raise_for_status()
        return response.json()

    def publish_transition(
        self,
        *,
        object_type: str,
        track_id: int,
        from_zone: str,
        to_zone: str,
        timestamp: str,
    ) -> dict:
        response = requests.post(
            f"{self.backend_base_url}/api/transitions",
            json={
                "object_type": object_type,
                "track_id": track_id,
                "from_zone": from_zone,
                "to_zone": to_zone,
                "timestamp": timestamp,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def sync_tracks(self, tracks: list[dict]) -> list[dict]:
        if not tracks:
            return []
        response = requests.post(
            f"{self.backend_base_url}/api/tracks/sync",
            json={"tracks": tracks},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
