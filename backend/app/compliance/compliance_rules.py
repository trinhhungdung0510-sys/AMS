from __future__ import annotations

from app.compliance.constants import COMPLIANCE_RULE_DEFINITIONS, COMPLIANCE_RULE_IDS, ComplianceRuleDefinition
from app.compliance.rule_registry import load_compliance_rules
from app.compliance.rules.base import BaseComplianceRule


def build_default_compliance_rules() -> list[BaseComplianceRule]:
    return load_compliance_rules()


def list_managed_rule_definitions() -> list[ComplianceRuleDefinition]:
    return list(COMPLIANCE_RULE_DEFINITIONS)


__all__ = [
    "COMPLIANCE_RULE_DEFINITIONS",
    "COMPLIANCE_RULE_IDS",
    "ComplianceRuleDefinition",
    "build_default_compliance_rules",
    "list_managed_rule_definitions",
]
