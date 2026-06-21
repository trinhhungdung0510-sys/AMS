from __future__ import annotations

from abc import ABC, abstractmethod

from app.compliance.types import ComplianceContext, ComplianceEvaluationResult


class BaseComplianceRule(ABC):
    id: str
    name: str
    event_type: str
    enabled: bool = True

    @abstractmethod
    def evaluate(self, context: ComplianceContext) -> ComplianceEvaluationResult:
        raise NotImplementedError("evaluate() must be implemented")
