from __future__ import annotations

from typing import Literal, Optional

PRESENCE_UNKNOWN = "UNKNOWN"
PRESENCE_OUTSIDE = "OUTSIDE"
PRESENCE_INSIDE = "INSIDE"

PRESENCE_ENTER = "enter"
PRESENCE_EXIT = "exit"

Transition = Literal["enter", "exit"]


def presence_key(camera_id: str, track_id: str, zone_id: str) -> str:
    return f"{camera_id}:{track_id}:{zone_id}"


class ZonePresenceTracker:
    def __init__(self) -> None:
        self._states: dict[str, str] = {}

    def get_state(self, camera_id: str, track_id: str, zone_id: str) -> str:
        return self._states.get(presence_key(camera_id, track_id, zone_id), PRESENCE_UNKNOWN)

    def update(self, camera_id: str, track_id: str, zone_id: str, is_inside: bool) -> Optional[Transition]:
        key = presence_key(camera_id, track_id, zone_id)
        current = self.get_state(camera_id, track_id, zone_id)
        next_state = PRESENCE_INSIDE if is_inside else PRESENCE_OUTSIDE

        if current == next_state:
            return None

        self._states[key] = next_state

        if next_state == PRESENCE_INSIDE and current in (PRESENCE_UNKNOWN, PRESENCE_OUTSIDE):
            return PRESENCE_ENTER
        if next_state == PRESENCE_OUTSIDE and current == PRESENCE_INSIDE:
            return PRESENCE_EXIT
        return None

    def clear(self) -> None:
        self._states.clear()


_tracker: ZonePresenceTracker | None = None


def get_zone_presence_tracker() -> ZonePresenceTracker:
    global _tracker
    if _tracker is None:
        _tracker = ZonePresenceTracker()
    return _tracker
