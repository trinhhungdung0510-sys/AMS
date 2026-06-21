from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.biosecurity_workflow.constants import BIOSECURITY_PROCESS_VIOLATION, WORKFLOW_STEP_CODES
from app.biosecurity_workflow.workflow_engine import BiosecurityWorkflowEngine, WorkflowEvaluationContext
from app.biosecurity_workflow.workflow_manager import init_workflow_manager
from app.biosecurity_workflow.workflow_state_store import get_workflow_state_store


@pytest.fixture(autouse=True)
def reset_workflow_state():
    init_workflow_manager()
    store = get_workflow_state_store()
    store._states.clear()
    yield
    store._states.clear()


def _context(**overrides):
    base = {
        "camera_id": "CAM-001",
        "track_id": 42,
        "zone_code": "shower_room",
        "timestamp": "2026-06-18T10:00:00+00:00",
        "object_type": "person",
    }
    base.update(overrides)
    return WorkflowEvaluationContext(**base)


def test_compliant_step_sequence():
    engine = BiosecurityWorkflowEngine()
    zones = [
        "shower_room",
        "handwash_zone",
        "boot_disinfection_tray",
        "gestation_barn",
    ]

    for zone_code in zones:
        results = engine.evaluate(_context(zone_code=zone_code))
        assert len(results) == 1
        assert results[0].compliant is True
        assert results[0].violated is False


def test_skip_shower_triggers_process_violation():
    engine = BiosecurityWorkflowEngine()
    results = engine.evaluate(_context(zone_code="handwash_zone"))

    assert len(results) == 1
    result = results[0]
    assert result.violated is True
    assert result.event_type == BIOSECURITY_PROCESS_VIOLATION
    assert WORKFLOW_STEP_CODES["ENTER_SHOWER"] in result.skipped_steps


def test_skip_boot_sanitization_before_clean_zone():
    engine = BiosecurityWorkflowEngine()
    engine.evaluate(_context(zone_code="shower_room"))
    engine.evaluate(_context(zone_code="handwash_zone"))
    results = engine.evaluate(_context(zone_code="gestation_barn"))

    assert len(results) == 1
    result = results[0]
    assert result.violated is True
    assert WORKFLOW_STEP_CODES["BOOT_SANITIZATION"] in result.skipped_steps


def test_non_person_skips_evaluation():
    engine = BiosecurityWorkflowEngine()
    assert engine.evaluate(_context(object_type="dog", zone_code="gestation_barn")) == []


@patch("app.biosecurity_workflow.integration.create_compliance_violation_event")
def test_integration_emits_compliance_event(mock_create_event):
    from app.biosecurity_workflow.integration import evaluate_biosecurity_process

    mock_event = SimpleNamespace(id="EVT-001")
    mock_create_event.return_value = mock_event
    db = MagicMock()

    transition = SimpleNamespace(
        id="ZT-001",
        camera_id="CAM-001",
        track_id=99,
        to_zone="gestation_barn",
        from_zone="handwash_zone",
        cross_time="2026-06-18T10:05:00+00:00",
        object_type="person",
    )

    payload = evaluate_biosecurity_process(db, transition)

    assert payload is not None
    assert payload["type"] == BIOSECURITY_PROCESS_VIOLATION
    assert payload["event_id"] == "EVT-001"
    mock_create_event.assert_called_once()
    kwargs = mock_create_event.call_args.kwargs
    assert kwargs["event_type"] == BIOSECURITY_PROCESS_VIOLATION
    assert kwargs["rule_id"] == "entry_clean_zone"
