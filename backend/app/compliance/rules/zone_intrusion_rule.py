from __future__ import annotations

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.compliance.rules.base import BaseComplianceRule
from app.compliance.types import ComplianceContext, ComplianceEvaluationResult
from app.data.biosecurity_ai_v40 import RESTRICTED_BIOSECURITY_LEVELS
from app.services.atsh_biosecurity_engine import _resolve_zone_meta


class ZoneIntrusionRule(BaseComplianceRule):
    """Wraps forbidden-zone intrusion check from ATSH engine without modifying it."""

    id = COMPLIANCE_RULE_IDS["ZONE_INTRUSION"]
    name = "Xâm nhập vùng cấm"
    event_type = "ZONE_INTRUSION"

    def evaluate(self, context: ComplianceContext) -> ComplianceEvaluationResult:
        transition = context.transition
        if transition is None:
            return ComplianceEvaluationResult(violated=False, score=0.0, evidence={})

        to_meta = _resolve_zone_meta(context.db, transition.to_zone)
        violated = self._matches_forbidden_zone(transition, to_meta)
        if not violated:
            return ComplianceEvaluationResult(violated=False, score=0.0, evidence={})

        return ComplianceEvaluationResult(
            violated=True,
            score=0.99,
            evidence={
                "source": "atsh_forbidden_zone_intrusion",
                "from_zone": transition.from_zone,
                "to_zone": transition.to_zone,
                "object_type": transition.object_type,
                "track_id": transition.track_id,
                "biosecurity_level": to_meta.get("biosecurity_level"),
            },
        )

    @staticmethod
    def _matches_forbidden_zone(transition, to_meta: dict) -> bool:
        """Same predicate as ``atsh_biosecurity_engine._eval_forbidden_zone`` — read-only wrap."""
        if transition.object_type.lower() != "person":
            return False

        to_level = to_meta.get("biosecurity_level", "")
        to_zone = transition.to_zone
        return to_level in RESTRICTED_BIOSECURITY_LEVELS or to_zone in {
            "feed_storage",
            "vet_medicine_storage",
            "quarantine_barn",
        }
