from __future__ import annotations

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.compliance.rules.base import BaseComplianceRule
from app.compliance.types import ComplianceContext, ComplianceEvaluationResult


class BiosecurityProcessRule(BaseComplianceRule):
    """Workflow process violations are evaluated by biosecurity_workflow engine."""

    id = COMPLIANCE_RULE_IDS["BIOSECURITY_PROCESS_VIOLATION"]
    name = "Vi phạm quy trình an toàn sinh học"
    event_type = "BIOSECURITY_PROCESS_VIOLATION"

    def evaluate(self, context: ComplianceContext) -> ComplianceEvaluationResult:
        return ComplianceEvaluationResult(violated=False, score=0.0, evidence={})
