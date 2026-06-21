"""Re-export — compliance events are created via evaluator_event_service."""

from app.services.evaluator_event_service import create_compliance_violation_event

__all__ = ["create_compliance_violation_event"]
