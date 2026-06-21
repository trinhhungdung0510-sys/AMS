from __future__ import annotations

from dataclasses import dataclass

from app.core.config import get_settings


@dataclass(frozen=True)
class ComplianceSettings:
    uniform_threshold: float = 0.85
    save_evidence: bool = True
    evidence_subdir: str = "evidence"


def get_compliance_settings() -> ComplianceSettings:
    settings = get_settings()
    return ComplianceSettings(
        uniform_threshold=getattr(settings, "compliance_uniform_threshold", 0.85),
        save_evidence=getattr(settings, "compliance_save_evidence", True),
        evidence_subdir=getattr(settings, "compliance_evidence_subdir", "evidence"),
    )
