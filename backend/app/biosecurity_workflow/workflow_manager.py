from __future__ import annotations

import logging

from app.biosecurity_workflow.definitions import DEFAULT_WORKFLOW_DEFINITIONS, WorkflowDefinition

logger = logging.getLogger(__name__)


class WorkflowManager:
    def __init__(self) -> None:
        self._definitions: dict[str, WorkflowDefinition] = {}

    def register_definition(self, definition: WorkflowDefinition) -> None:
        self._definitions[definition.id] = definition

    def get_definition(self, workflow_id: str) -> WorkflowDefinition | None:
        return self._definitions.get(workflow_id)

    def list_definitions(self) -> list[WorkflowDefinition]:
        return list(self._definitions.values())

    def load_defaults(self) -> None:
        for definition in DEFAULT_WORKFLOW_DEFINITIONS:
            self.register_definition(definition)
        logger.info(
            "Biosecurity Workflow Manager loaded %s definitions: %s",
            len(self._definitions),
            ", ".join(self._definitions.keys()),
        )


_manager: WorkflowManager | None = None


def init_workflow_manager() -> WorkflowManager:
    global _manager
    _manager = WorkflowManager()
    _manager.load_defaults()
    return _manager


def get_workflow_manager() -> WorkflowManager:
    if _manager is None:
        return init_workflow_manager()
    return _manager
