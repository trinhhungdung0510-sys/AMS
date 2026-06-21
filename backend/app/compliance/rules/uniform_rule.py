from __future__ import annotations

from app.compliance.compliance_rules import COMPLIANCE_RULE_IDS
from app.compliance.config import get_compliance_settings
from app.compliance.rules.base import BaseComplianceRule
from app.compliance.types import ComplianceContext, ComplianceEvaluationResult
from app.compliance.uniform_matcher import match_uniform
from app.models import CameraZone, UniformTemplate


class UniformRule(BaseComplianceRule):
    id = COMPLIANCE_RULE_IDS["UNIFORM_VIOLATION"]
    name = "Sai đồng phục bảo hộ"
    event_type = "UNIFORM_VIOLATION"

    def evaluate(self, context: ComplianceContext) -> ComplianceEvaluationResult:
        if context.metadata.get("trigger_event") != "PERSON_ENTER":
            return ComplianceEvaluationResult(violated=False, score=0.0, evidence={})

        zone = context.db.get(CameraZone, context.zone_id)
        if not zone or not zone.required_uniform_id:
            return ComplianceEvaluationResult(
                violated=False,
                score=1.0,
                evidence={"reason": "no_required_uniform"},
            )

        template = context.db.get(UniformTemplate, zone.required_uniform_id)
        if not template:
            return ComplianceEvaluationResult(
                violated=False,
                score=0.0,
                evidence={"reason": "template_not_found", "required_uniform_id": zone.required_uniform_id},
            )

        person_image = context.metadata.get("person_snapshot")
        if isinstance(person_image, str):
            person_image = person_image.encode("utf-8")

        settings = get_compliance_settings()
        match = match_uniform(
            person_image,
            template.image_paths or [],
            track_id=context.track_id,
            template_id=template.id,
            threshold=settings.uniform_threshold,
        )

        if match.score >= settings.uniform_threshold:
            return ComplianceEvaluationResult(
                violated=False,
                score=match.score,
                evidence={
                    "required_uniform_id": template.id,
                    "required_uniform_name": template.name,
                    "matched": match.matched,
                },
            )

        return ComplianceEvaluationResult(
            violated=True,
            score=match.score,
            evidence={
                "event_type": self.event_type,
                "required_uniform_id": template.id,
                "required_uniform_name": template.name,
                "matched": match.matched,
                "threshold": settings.uniform_threshold,
            },
        )
