from __future__ import annotations

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.compliance.rules.base import BaseComplianceRule
from app.compliance.types import ComplianceContext, ComplianceEvaluationResult
from app.data.animal_intrusion import ANIMAL_OBJECT_TYPES
from app.services.animal_intrusion_engine import normalize_zone_code


class AnimalIntrusionRule(BaseComplianceRule):
    """Wraps animal intrusion policy check without modifying ``animal_intrusion_engine``."""

    id = COMPLIANCE_RULE_IDS["ANIMAL_INTRUSION"]
    name = "Động vật xâm nhập"
    event_type = "ANIMAL_INTRUSION"

    def evaluate(self, context: ComplianceContext) -> ComplianceEvaluationResult:
        transition = context.transition
        if transition is None:
            return ComplianceEvaluationResult(violated=False, score=0.0, evidence={})

        object_type = transition.object_type.lower()
        if object_type not in ANIMAL_OBJECT_TYPES:
            return ComplianceEvaluationResult(violated=False, score=0.0, evidence={})

        from sqlalchemy import select

        from app.models import AnimalIntrusionPolicy

        policy = context.db.scalar(
            select(AnimalIntrusionPolicy)
            .where(AnimalIntrusionPolicy.object_type == object_type)
            .where(AnimalIntrusionPolicy.enabled.is_(True))
            .limit(1)
        )
        if not policy:
            return ComplianceEvaluationResult(violated=False, score=0.0, evidence={})

        to_zone = normalize_zone_code(transition.to_zone)
        allowed_zones = {normalize_zone_code(zone) for zone in policy.allowed_zones}
        restricted_zones = {normalize_zone_code(zone) for zone in policy.restricted_zones}

        violation_reason = None
        if to_zone in restricted_zones:
            violation_reason = "restricted_zone_entry"
        elif allowed_zones and to_zone not in allowed_zones:
            violation_reason = "outside_allowed_zone"

        if not violation_reason:
            return ComplianceEvaluationResult(violated=False, score=0.0, evidence={})

        return ComplianceEvaluationResult(
            violated=True,
            score=0.99,
            evidence={
                "source": "animal_intrusion_policy",
                "object_type": object_type,
                "violation_reason": violation_reason,
                "to_zone": to_zone,
                "track_id": transition.track_id,
            },
        )
