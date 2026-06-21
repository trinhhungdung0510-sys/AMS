from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.compliance.compliance_engine import ComplianceEngine
from app.compliance.constants import COMPLIANCE_RULE_IDS, ComplianceRuleDefinition
from app.compliance.compliance_rules import build_default_compliance_rules, list_managed_rule_definitions
from app.compliance.rules.hand_sanitation_rule import HandSanitationRule
from app.compliance.rules.uniform_rule import UniformRule
from app.compliance.rules.zone_intrusion_rule import ZoneIntrusionRule
from app.compliance.types import ComplianceContext


def test_managed_rule_catalog_has_seven_entries():
    definitions = list_managed_rule_definitions()
    assert len(definitions) == 7
    assert {item.id for item in definitions} == set(COMPLIANCE_RULE_IDS.values())


def test_default_engine_registers_all_rules():
    engine = ComplianceEngine()
    assert len(engine.rules) == 7
    assert engine.list_managed_rules()[0]["id"] == COMPLIANCE_RULE_IDS["ZONE_INTRUSION"]


def test_skeleton_rules_return_not_violated():
    context = ComplianceContext(db=MagicMock(), camera_id="CAM-001")
    for rule in [HandSanitationRule(), UniformRule()]:
        result = rule.evaluate(context)
        assert result.violated is False
        assert result.score == 0.0


def test_zone_intrusion_wraps_existing_predicate():
    transition = SimpleNamespace(
        object_type="person",
        to_zone="feed_storage",
        from_zone="farm_gate",
        track_id=7,
        cross_time="2026-06-18T10:00:00+00:00",
    )
    violated = ZoneIntrusionRule._matches_forbidden_zone(transition, {"biosecurity_level": "clean"})
    assert violated is True

    safe_transition = SimpleNamespace(
        object_type="person",
        to_zone="gestation_barn",
        from_zone="farm_gate",
        track_id=8,
        cross_time="2026-06-18T10:01:00+00:00",
    )
    assert ZoneIntrusionRule._matches_forbidden_zone(safe_transition, {"biosecurity_level": "clean"}) is False


def test_zone_intrusion_skips_non_person():
    transition = SimpleNamespace(object_type="dog", to_zone="feed_storage")
    assert ZoneIntrusionRule._matches_forbidden_zone(transition, {}) is False


def test_compliance_engine_evaluate_without_transition_returns_empty():
    engine = ComplianceEngine(build_default_compliance_rules())
    context = ComplianceContext(db=MagicMock(), camera_id="CAM-001")
    assert engine.evaluate(context, publish=False) == []


def test_violation_event_shape():
    engine = ComplianceEngine([ZoneIntrusionRule()])
    db = MagicMock()
    db.get.return_value = SimpleNamespace(farm_id="FARM-001")
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock(side_effect=lambda event: event)

    transition = SimpleNamespace(
        object_type="person",
        to_zone="feed_storage",
        from_zone="farm_gate",
        track_id=3,
        cross_time="2026-06-18T10:00:00+00:00",
        camera_id="CAM-001",
    )
    context = ComplianceContext(
        db=db,
        camera_id="CAM-001",
        transition=transition,
        timestamp=transition.cross_time,
    )

    violations = engine.evaluate(context, publish=False)
    assert len(violations) == 1
    payload = violations[0].to_dict()
    assert payload["eventType"] == "ZONE_INTRUSION"
    assert payload["ruleId"] == COMPLIANCE_RULE_IDS["ZONE_INTRUSION"]
    assert payload["cameraId"] == "CAM-001"
    assert payload["zoneId"] == "feed_storage"
    assert payload["trackId"] == 3
    assert payload["score"] == 0.99
    assert payload["snapshotPath"] is None
