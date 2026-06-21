from __future__ import annotations

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.compliance.rules.base import BaseComplianceRule
from app.compliance.types import ComplianceContext, ComplianceEvaluationResult


class BootSanitationRule(BaseComplianceRule):
    """Skeleton — v1.8 will implement boot disinfection workflow checks."""

    id = COMPLIANCE_RULE_IDS["NO_BOOT_SANITIZATION"]
    name = "Không sát trùng ủng"
    event_type = "NO_BOOT_SANITIZATION"

    def evaluate(self, context: ComplianceContext) -> ComplianceEvaluationResult:
        return ComplianceEvaluationResult(violated=False, score=0.0, evidence={})
