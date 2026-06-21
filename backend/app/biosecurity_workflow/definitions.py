from __future__ import annotations

from dataclasses import dataclass, field

from app.biosecurity_workflow.constants import (
    CLEAN_PRODUCTION_ZONES,
    STEP_ZONE_CODES,
    WORKFLOW_STEP_CODES,
)


@dataclass(frozen=True)
class WorkflowDefinition:
    id: str
    name: str
    steps: list[str]
    step_zones: dict[str, str] = field(default_factory=dict)

    def zone_for_step(self, step_code: str) -> str | None:
        if step_code in self.step_zones:
            return self.step_zones[step_code]
        if step_code == WORKFLOW_STEP_CODES["ENTER_CLEAN_ZONE"]:
            return None
        return STEP_ZONE_CODES.get(step_code)

    def step_for_zone(self, zone_code: str) -> str | None:
        for step_code in self.steps:
            mapped = self.zone_for_step(step_code)
            if mapped and mapped == zone_code:
                return step_code
        if zone_code in CLEAN_PRODUCTION_ZONES and WORKFLOW_STEP_CODES["ENTER_CLEAN_ZONE"] in self.steps:
            return WORKFLOW_STEP_CODES["ENTER_CLEAN_ZONE"]
        return None


ENTRY_CLEAN_ZONE_WORKFLOW = WorkflowDefinition(
    id="entry_clean_zone",
    name="Quy trình vào vùng sạch",
    steps=[
        WORKFLOW_STEP_CODES["ENTER_SHOWER"],
        WORKFLOW_STEP_CODES["HAND_SANITIZATION"],
        WORKFLOW_STEP_CODES["BOOT_SANITIZATION"],
        WORKFLOW_STEP_CODES["ENTER_CLEAN_ZONE"],
    ],
)

DEFAULT_WORKFLOW_DEFINITIONS: tuple[WorkflowDefinition, ...] = (ENTRY_CLEAN_ZONE_WORKFLOW,)
