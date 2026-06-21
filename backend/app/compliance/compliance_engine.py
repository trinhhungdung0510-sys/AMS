from __future__ import annotations

import logging
from typing import Iterable

from app.compliance.compliance_rules import list_managed_rule_definitions
from app.compliance.config import get_compliance_settings
from app.compliance.evidence_snapshot import save_evidence_snapshot
from app.compliance.rule_registry import load_compliance_rules
from app.compliance.rules.base import BaseComplianceRule
from app.compliance.types import ComplianceContext, ComplianceEvaluationResult, ComplianceViolationEvent
from app.services.evaluator_event_service import create_compliance_violation_event

logger = logging.getLogger(__name__)

_engine: "ComplianceEngine | None" = None


class ComplianceEngine:
    """Runs registered compliance rules sequentially and emits unified violation events."""

    def __init__(self, rules: Iterable[BaseComplianceRule] | None = None) -> None:
        self._rules: list[BaseComplianceRule] = list(rules or load_compliance_rules())

    @property
    def rules(self) -> list[BaseComplianceRule]:
        return list(self._rules)

    def register_rule(self, rule: BaseComplianceRule) -> None:
        self._rules.append(rule)

    def list_managed_rules(self) -> list[dict[str, str]]:
        return [
            {"id": rule.id, "name": rule.name, "event_type": rule.event_type, "enabled": str(rule.enabled)}
            for rule in self._rules
        ]

    def evaluate(self, context: ComplianceContext, *, publish: bool = True) -> list[ComplianceViolationEvent]:
        violations: list[ComplianceViolationEvent] = []

        for rule in self._rules:
            if not rule.enabled:
                continue

            result = rule.evaluate(context)
            self._log_result(rule, context, result)

            if not result.violated:
                continue

            violation = self._build_violation_event(rule, context, result)
            violations.append(violation)
            self.emit_violation(context, violation, publish=publish)

        return violations

    def emit_violation(
        self,
        context: ComplianceContext,
        violation: ComplianceViolationEvent,
        *,
        publish: bool = True,
    ) -> None:
        settings = get_compliance_settings()
        snapshot_path = violation.snapshot_path
        if settings.save_evidence and not snapshot_path:
            snapshot_path = save_evidence_snapshot(
                timestamp=violation.timestamp,
                bbox=context.metadata.get("bbox"),
                label=violation.rule_name,
            )

        create_compliance_violation_event(
            context.db,
            event_type=violation.event_type,
            rule_id=violation.rule_id,
            rule_name=violation.rule_name,
            camera_id=violation.camera_id,
            zone_id=violation.zone_id,
            track_id=violation.track_id,
            score=violation.score,
            snapshot_path=snapshot_path,
            timestamp=violation.timestamp,
            evidence=violation.evidence,
            publish=publish,
        )

    def _build_violation_event(
        self,
        rule: BaseComplianceRule,
        context: ComplianceContext,
        result: ComplianceEvaluationResult,
    ) -> ComplianceViolationEvent:
        zone_id = context.zone_id
        if not zone_id and context.transition is not None:
            zone_id = context.transition.to_zone

        timestamp = context.timestamp
        if not timestamp and context.transition is not None:
            timestamp = context.transition.cross_time

        track_id = context.track_id
        if track_id is None and context.transition is not None:
            track_id = context.transition.track_id

        snapshot_path = context.metadata.get("snapshot_path") or context.metadata.get("snapshotPath")

        return ComplianceViolationEvent(
            event_type=rule.event_type,
            rule_id=rule.id,
            rule_name=rule.name,
            camera_id=context.camera_id,
            zone_id=zone_id,
            track_id=track_id,
            score=result.score,
            snapshot_path=snapshot_path,
            timestamp=timestamp,
            evidence=result.evidence,
        )

    @staticmethod
    def _log_result(
        rule: BaseComplianceRule,
        context: ComplianceContext,
        result: ComplianceEvaluationResult,
    ) -> None:
        zone_label = context.metadata.get("zone_name") or context.zone_id or "-"
        logger.info(
            "[Compliance] Rule: %s Track: %s Zone: %s Score: %.2f Result: %s",
            rule.name,
            context.track_id if context.track_id is not None else "-",
            zone_label,
            result.score,
            "VIOLATED" if result.violated else "PASSED",
        )


def init_compliance_engine() -> ComplianceEngine:
    global _engine
    _engine = ComplianceEngine()
    managed = list_managed_rule_definitions()
    logger.info(
        "Compliance Engine initialized with %s rules: %s",
        len(_engine.rules),
        ", ".join(item.id for item in managed),
    )
    return _engine


def get_compliance_engine() -> ComplianceEngine:
    if _engine is None:
        return init_compliance_engine()
    return _engine
