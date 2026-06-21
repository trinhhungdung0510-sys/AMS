from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol

from sqlalchemy.orm import Session

from app.models import ZoneTransition


@dataclass(frozen=True)
class ComplianceEvaluationResult:
    violated: bool
    score: float
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ComplianceViolationEvent:
    event_type: str
    rule_id: str
    rule_name: str
    camera_id: str
    zone_id: str
    track_id: Optional[int]
    score: float
    snapshot_path: Optional[str]
    timestamp: str
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "eventType": self.event_type,
            "ruleId": self.rule_id,
            "ruleName": self.rule_name,
            "cameraId": self.camera_id,
            "zoneId": self.zone_id,
            "trackId": self.track_id,
            "score": self.score,
            "snapshotPath": self.snapshot_path,
            "timestamp": self.timestamp,
            "evidence": self.evidence,
        }


@dataclass
class ComplianceContext:
    db: Session
    camera_id: str
    zone_id: str = ""
    track_id: Optional[int] = None
    timestamp: str = ""
    transition: Optional[ZoneTransition] = None
    observation: Optional[dict[str, Any]] = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ComplianceRule(Protocol):
    id: str
    name: str
    enabled: bool

    def evaluate(self, context: ComplianceContext) -> ComplianceEvaluationResult: ...
