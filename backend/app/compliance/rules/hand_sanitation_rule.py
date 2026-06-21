from __future__ import annotations

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.compliance.rules.base import BaseComplianceRule
from app.compliance.types import ComplianceContext, ComplianceEvaluationResult


class HandSanitationRule(BaseComplianceRule):
    """Skeleton — v1.8 will implement hand sanitation workflow checks."""

    id = COMPLIANCE_RULE_IDS["NO_HAND_SANITIZATION"]
    name = "Không rửa tay sát trùng"
    event_type = "NO_HAND_SANITIZATION"

    def evaluate(self, context: ComplianceContext) -> ComplianceEvaluationResult:
        return ComplianceEvaluationResult(violated=False, score=0.0, evidence={})
