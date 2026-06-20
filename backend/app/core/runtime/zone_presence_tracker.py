from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

PRESENCE_UNKNOWN = "UNKNOWN"
PRESENCE_OUTSIDE = "OUTSIDE"
PRESENCE_INSIDE = "INSIDE"

PRESENCE_ENTER = "enter"
PRESENCE_EXIT = "exit"

Transition = Literal["enter", "exit"]


def presence_key(camera_id: str, track_id: str, zone_id: str) -> str:
    return f"{camera_id}:{track_id}:{zone_id}"


@dataclass
class ZoneTransitionResult:
    transition: Optional[Transition]
    previous_state: str
    next_state: str
    zone_state: dict


class ZonePresenceTracker:
    def __init__(self) -> None:
        self._states: dict[str, str] = {}
        self._records: dict[str, dict] = {}

    def get_state(self, camera_id: str, track_id: str, zone_id: str) -> str:
        return self._states.get(presence_key(camera_id, track_id, zone_id), PRESENCE_UNKNOWN)

    def get_zone_state(self, camera_id: str, track_id: str, zone_id: str) -> dict:
        key = presence_key(camera_id, track_id, zone_id)
        record = self._records.get(key)
        if record:
            return dict(record)

        return {
            "trackId": track_id,
            "cameraId": camera_id,
            "zoneId": zone_id,
            "currentZoneId": None,
            "previousZoneId": None,
            "state": PRESENCE_UNKNOWN,
            "enteredAt": None,
            "exitedAt": None,
        }

    def update(
        self,
        camera_id: str,
        track_id: str,
        zone_id: str,
        is_inside: bool,
        timestamp: str | None = None,
    ) -> ZoneTransitionResult:
        key = presence_key(camera_id, track_id, zone_id)
        current = self.get_state(camera_id, track_id, zone_id)
        previous_record = self.get_zone_state(camera_id, track_id, zone_id)
        next_state = PRESENCE_INSIDE if is_inside else PRESENCE_OUTSIDE
        transition: Optional[Transition] = None

        if current == next_state:
            record = dict(previous_record)
            record["state"] = current
            self._records[key] = record
            return ZoneTransitionResult(
                transition=None,
                previous_state=current,
                next_state=current,
                zone_state=record,
            )

        if next_state == PRESENCE_INSIDE and current == PRESENCE_OUTSIDE:
            transition = PRESENCE_ENTER
        elif next_state == PRESENCE_OUTSIDE and current == PRESENCE_INSIDE:
            transition = PRESENCE_EXIT

        previous_zone_id = previous_record.get("currentZoneId")
        record = {
            "trackId": track_id,
            "cameraId": camera_id,
            "zoneId": zone_id,
            "currentZoneId": zone_id if is_inside else None,
            "previousZoneId": previous_zone_id if is_inside else zone_id,
            "state": next_state,
            "enteredAt": timestamp if is_inside else previous_record.get("enteredAt"),
            "exitedAt": None if is_inside else timestamp,
        }

        if is_inside and transition == PRESENCE_ENTER:
            record["enteredAt"] = timestamp
            record["exitedAt"] = None
        elif not is_inside and transition == PRESENCE_EXIT:
            record["exitedAt"] = timestamp

        self._states[key] = next_state
        self._records[key] = record

        return ZoneTransitionResult(
            transition=transition,
            previous_state=current,
            next_state=next_state,
            zone_state=record,
        )

    def apply_zones(
        self,
        camera_id: str,
        track_id: str,
        active_zone_ids: set[str],
        timestamp: str,
        monitored_zone_ids: set[str] | None = None,
    ) -> dict[str, ZoneTransitionResult]:
        prefix = f"{camera_id}:{track_id}:"
        known_zone_ids = {
            key.rsplit(":", 1)[-1]
            for key in self._states
            if key.startswith(prefix)
        }
        zone_ids = set(active_zone_ids) | known_zone_ids
        if monitored_zone_ids:
            zone_ids |= set(monitored_zone_ids)

        return {
            zone_id: self.update(
                camera_id,
                track_id,
                zone_id,
                zone_id in active_zone_ids,
                timestamp,
            )
            for zone_id in zone_ids
        }

    def clear(self) -> None:
        self._states.clear()
        self._records.clear()


_tracker: ZonePresenceTracker | None = None


def get_zone_presence_tracker() -> ZonePresenceTracker:
    global _tracker
    if _tracker is None:
        _tracker = ZonePresenceTracker()
    return _tracker
