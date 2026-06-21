from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.compliance.compliance_engine import ComplianceEngine
from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.compliance.evidence_snapshot import save_evidence_snapshot
from app.compliance.rule_registry import load_compliance_rules
from app.compliance.rules.uniform_rule import UniformRule
from app.compliance.types import ComplianceContext
from app.compliance.uniform_matcher import match_uniform
from app.models import CameraZone, UniformTemplate


def test_matcher_score_range():
    result = match_uniform(None, ["a.jpg"], track_id=12, template_id="uniform-clean")
    assert 0.75 <= result.score <= 0.99


def test_uniform_rule_passes_when_no_required_uniform():
    db = MagicMock()
    db.get.return_value = CameraZone(
        id="Z-1",
        camera_id="CAM-001",
        name="Clean Zone",
        zone_type="clean",
        points=[],
        color="#00ff00",
        points_format="pixel",
        created_at="",
        updated_at="",
        required_uniform_id=None,
    )
    rule = UniformRule()
    context = ComplianceContext(
        db=db,
        camera_id="CAM-001",
        zone_id="Z-1",
        track_id=12,
        metadata={"trigger_event": "PERSON_ENTER", "zone_name": "clean-zone"},
    )
    result = rule.evaluate(context)
    assert result.violated is False


def test_uniform_rule_violation_with_template():
    zone = CameraZone(
        id="Z-1",
        camera_id="CAM-001",
        name="clean-zone",
        zone_type="clean",
        points=[],
        color="#00ff00",
        points_format="pixel",
        created_at="",
        updated_at="",
        required_uniform_id="uniform-clean",
    )
    template = UniformTemplate(
        id="uniform-clean",
        name="Đồng phục vùng sạch",
        description="",
        image_paths=["/storage/uniforms/uniform-clean/1.jpg"],
        created_at="",
        updated_at="",
    )

    db = MagicMock()

    def _get(model, key):
        if model is CameraZone and key == "Z-1":
            return zone
        if model is UniformTemplate and key == "uniform-clean":
            return template
        return None

    db.get.side_effect = _get

    rule = UniformRule()
    context = ComplianceContext(
        db=db,
        camera_id="CAM-001",
        zone_id="Z-1",
        track_id=99,
        timestamp="2026-06-18T10:00:00+00:00",
        metadata={"trigger_event": "PERSON_ENTER", "zone_name": "clean-zone"},
    )
    result = rule.evaluate(context)
    assert result.score >= 0.75
    if result.score < 0.85:
        assert result.violated is True
    else:
        assert result.violated is False


def test_engine_register_and_evaluate():
    engine = ComplianceEngine([UniformRule()])
    assert len(engine.rules) == 1
    engine.register_rule(UniformRule())
    assert len(engine.rules) == 2


def test_registry_loads_seven_rules():
    assert len(load_compliance_rules()) == 7


def main() -> None:
    test_matcher_score_range()
    test_uniform_rule_passes_when_no_required_uniform()
    test_uniform_rule_violation_with_template()
    test_engine_register_and_evaluate()
    test_registry_loads_seven_rules()
    print("PHASE 3 COMPLIANCE TESTS PASSED")


if __name__ == "__main__":
    main()
