from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from app.biosecurity_workflow.constants import BIOSECURITY_PROCESS_VIOLATION, STEP_LABELS_VI
from app.biosecurity_workflow.definitions import WorkflowDefinition
from app.biosecurity_workflow.workflow_manager import get_workflow_manager
from app.biosecurity_workflow.workflow_state_store import get_workflow_state_store

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class WorkflowEvaluationResult:
    workflow_id: str
    workflow_name: str
    compliant: bool
    violated: bool = False
    event_type: str | None = None
    score: float = 1.0
    current_step: str | None = None
    skipped_steps: list[str] = field(default_factory=list)
    completed_steps: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowEvaluationContext:
    camera_id: str
    track_id: int
    zone_code: str
    timestamp: str
    object_type: str = "person"
    workflow_id: str | None = None


class BiosecurityWorkflowEngine:
    def __init__(self) -> None:
        self._manager = get_workflow_manager()
        self._store = get_workflow_state_store()

    def evaluate(self, context: WorkflowEvaluationContext) -> list[WorkflowEvaluationResult]:
        if context.object_type.lower() != "person":
            return []

        results: list[WorkflowEvaluationResult] = []
        definitions = (
            [self._manager.get_definition(context.workflow_id)]
            if context.workflow_id
            else self._manager.list_definitions()
        )

        for definition in definitions:
            if definition is None:
                continue
            result = self._evaluate_definition(context, definition)
            if result is not None:
                results.append(result)
        return results

    def _evaluate_definition(
        self,
        context: WorkflowEvaluationContext,
        definition: WorkflowDefinition,
    ) -> WorkflowEvaluationResult | None:
        step_code = definition.step_for_zone(context.zone_code)
        if step_code is None:
            return None

        state = self._store.get_state(context.camera_id, context.track_id, definition.id)
        completed = list(state.completed_steps)

        if step_code in completed:
            return WorkflowEvaluationResult(
                workflow_id=definition.id,
                workflow_name=definition.name,
                compliant=True,
                current_step=step_code,
                completed_steps=completed,
                evidence={"status": "step_already_completed", "step": step_code},
            )

        expected_index = len(completed)
        actual_index = definition.steps.index(step_code)
        skipped = definition.steps[expected_index:actual_index]

        if skipped:
            skipped_labels = [STEP_LABELS_VI.get(code, code) for code in skipped]
            logger.warning(
                "[Workflow] VIOLATION workflow=%s track=%s skipped=%s attempted=%s",
                definition.id,
                context.track_id,
                skipped,
                step_code,
            )
            return WorkflowEvaluationResult(
                workflow_id=definition.id,
                workflow_name=definition.name,
                compliant=False,
                violated=True,
                event_type=BIOSECURITY_PROCESS_VIOLATION,
                score=0.35,
                current_step=step_code,
                skipped_steps=skipped,
                completed_steps=completed,
                evidence={
                    "workflow_id": definition.id,
                    "workflow_name": definition.name,
                    "attempted_step": step_code,
                    "skipped_steps": skipped,
                    "skipped_step_labels": skipped_labels,
                    "zone_code": context.zone_code,
                },
            )

        updated = self._store.mark_step_completed(
            camera_id=context.camera_id,
            track_id=context.track_id,
            workflow_id=definition.id,
            step_code=step_code,
            zone_code=context.zone_code,
            timestamp=context.timestamp,
        )
        logger.info(
            "[Workflow] PASSED workflow=%s track=%s step=%s zone=%s",
            definition.id,
            context.track_id,
            step_code,
            context.zone_code,
        )
        return WorkflowEvaluationResult(
            workflow_id=definition.id,
            workflow_name=definition.name,
            compliant=True,
            violated=False,
            score=1.0,
            current_step=step_code,
            completed_steps=list(updated.completed_steps),
            evidence={"status": "step_completed", "step": step_code},
        )


_engine: BiosecurityWorkflowEngine | None = None


def get_biosecurity_workflow_engine() -> BiosecurityWorkflowEngine:
    global _engine
    if _engine is None:
        _engine = BiosecurityWorkflowEngine()
    return _engine
