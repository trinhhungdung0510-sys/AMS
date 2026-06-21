from __future__ import annotations

import logging
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.biosecurity_workflow.constants import BIOSECURITY_PROCESS_VIOLATION, STEP_LABELS_VI
from app.biosecurity_workflow.workflow_engine import (
    BiosecurityWorkflowEngine,
    WorkflowEvaluationContext,
    get_biosecurity_workflow_engine,
)
from app.models import ZoneTransition
from app.services.evaluator_event_service import create_compliance_violation_event

logger = logging.getLogger(__name__)


def evaluate_biosecurity_process(
    db: Session,
    transition: ZoneTransition,
    *,
    publish: bool = True,
) -> Optional[dict[str, Any]]:
    engine = get_biosecurity_workflow_engine()
    context = WorkflowEvaluationContext(
        camera_id=transition.camera_id,
        track_id=transition.track_id,
        zone_code=transition.to_zone,
        timestamp=transition.cross_time,
        object_type=transition.object_type,
    )

    results = engine.evaluate(context)
    violation = next((item for item in results if item.violated), None)
    if violation is None:
        return None

    skipped_labels = [
        STEP_LABELS_VI.get(code, code) for code in violation.skipped_steps
    ]
    rule_name = f"Vi phạm quy trình: {violation.workflow_name}"

    event = create_compliance_violation_event(
        db,
        event_type=BIOSECURITY_PROCESS_VIOLATION,
        rule_id=violation.workflow_id,
        rule_name=rule_name,
        camera_id=transition.camera_id,
        zone_id=transition.to_zone,
        track_id=transition.track_id,
        score=violation.score,
        snapshot_path=None,
        timestamp=transition.cross_time,
        evidence={
            **violation.evidence,
            "transition_id": transition.id,
            "from_zone": transition.from_zone,
            "to_zone": transition.to_zone,
            "skipped_steps": violation.skipped_steps,
            "skipped_step_labels": skipped_labels,
            "completed_steps": violation.completed_steps,
            "attempted_step": violation.current_step,
        },
        publish=publish,
    )

    return {
        "type": BIOSECURITY_PROCESS_VIOLATION,
        "event_id": event.id,
        "workflow_id": violation.workflow_id,
        "workflow_name": violation.workflow_name,
        "skipped_steps": violation.skipped_steps,
        "attempted_step": violation.current_step,
        "track_id": transition.track_id,
        "camera_id": transition.camera_id,
        "zone_code": transition.to_zone,
        "occurred_at": transition.cross_time,
    }
