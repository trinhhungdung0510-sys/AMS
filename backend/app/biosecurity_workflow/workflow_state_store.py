from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock


@dataclass
class TrackWorkflowState:
    workflow_id: str
    completed_steps: list[str] = field(default_factory=list)
    last_zone: str = ""
    updated_at: str = ""


class WorkflowStateStore:
    """In-memory workflow progress keyed by camera + track + workflow."""

    def __init__(self) -> None:
        self._states: dict[str, TrackWorkflowState] = {}
        self._lock = Lock()

    @staticmethod
    def _key(camera_id: str, track_id: int, workflow_id: str) -> str:
        return f"{camera_id}:{track_id}:{workflow_id}"

    def get_state(self, camera_id: str, track_id: int, workflow_id: str) -> TrackWorkflowState:
        key = self._key(camera_id, track_id, workflow_id)
        with self._lock:
            state = self._states.get(key)
            if state is None:
                state = TrackWorkflowState(workflow_id=workflow_id)
                self._states[key] = state
            return state

    def mark_step_completed(
        self,
        *,
        camera_id: str,
        track_id: int,
        workflow_id: str,
        step_code: str,
        zone_code: str,
        timestamp: str,
    ) -> TrackWorkflowState:
        state = self.get_state(camera_id, track_id, workflow_id)
        if step_code not in state.completed_steps:
            state.completed_steps.append(step_code)
        state.last_zone = zone_code
        state.updated_at = timestamp
        return state

    def reset(self, camera_id: str, track_id: int, workflow_id: str) -> None:
        key = self._key(camera_id, track_id, workflow_id)
        with self._lock:
            self._states.pop(key, None)


_store: WorkflowStateStore | None = None


def get_workflow_state_store() -> WorkflowStateStore:
    global _store
    if _store is None:
        _store = WorkflowStateStore()
    return _store
