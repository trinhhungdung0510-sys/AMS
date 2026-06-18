"""Extension pipeline for AMS ATSH engines (v3.1 → v3.4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models import TrackWorkflowProgress, Workflow, ZoneTransition


@dataclass
class WorkflowContext:
    """Shared context passed to downstream ATSH engines."""

    track_id: int
    camera_id: str
    transition: ZoneTransition
    zone_history: list[dict] = field(default_factory=list)
    workflow_progress: list[dict] = field(default_factory=list)
    active_workflows: list[dict] = field(default_factory=list)
    violation_payload: Optional[dict] = None


class ATSHPipeline:
    """Hook registry for Route (v3.2), Contact Risk (v3.3), ATSH Score (v3.4)."""

    def __init__(self) -> None:
        self._post_workflow_hooks: list[str] = [
            "route_engine_v32",
            "contact_risk_engine_v33",
            "atsh_score_engine_v34",
        ]

    @property
    def registered_engines(self) -> list[str]:
        return list(self._post_workflow_hooks)

    def run_post_workflow(self, db: Session, context: WorkflowContext) -> list[dict]:
        """Run downstream engines. Placeholders until v3.2–v3.4 are implemented."""
        results: list[dict] = []
        for engine in self._post_workflow_hooks:
            results.append(
                {
                    "engine": engine,
                    "status": "pending",
                    "track_id": context.track_id,
                    "camera_id": context.camera_id,
                    "transition_id": context.transition.id,
                }
            )
        return results


atsh_pipeline = ATSHPipeline()


def build_workflow_context(
    db: Session,
    transition: ZoneTransition,
    *,
    zone_history: list[dict],
    progress_rows: list[TrackWorkflowProgress],
    workflows: list[Workflow],
    violation_payload: Optional[dict] = None,
) -> WorkflowContext:
    return WorkflowContext(
        track_id=transition.track_id,
        camera_id=transition.camera_id,
        transition=transition,
        zone_history=zone_history,
        workflow_progress=[
            {
                "workflow_id": row.workflow_id,
                "completed_step_order": row.completed_step_order,
                "last_zone": row.last_zone,
                "updated_at": row.updated_at,
            }
            for row in progress_rows
        ],
        active_workflows=[
            {"id": workflow.id, "name": workflow.name, "enabled": workflow.enabled}
            for workflow in workflows
        ],
        violation_payload=violation_payload,
    )
