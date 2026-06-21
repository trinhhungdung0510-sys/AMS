from __future__ import annotations

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.compliance.rules.base import BaseComplianceRule
from app.compliance.types import ComplianceContext, ComplianceEvaluationResult


class VehicleSanitationRule(BaseComplianceRule):
    """Skeleton — v1.8 will implement vehicle intrusion / disinfection checks."""

    id = COMPLIANCE_RULE_IDS["VEHICLE_INTRUSION"]
    name = "Xe xâm nhập / chưa sát trùng"
    event_type = "VEHICLE_INTRUSION"

    def evaluate(self, context: ComplianceContext) -> ComplianceEvaluationResult:
        return ComplianceEvaluationResult(violated=False, score=0.0, evidence={})
