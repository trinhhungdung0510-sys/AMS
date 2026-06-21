from __future__ import annotations

from app.compliance.rules.animal_intrusion_rule import AnimalIntrusionRule
from app.compliance.rules.biosecurity_process_rule import BiosecurityProcessRule
from app.compliance.rules.base import BaseComplianceRule
from app.compliance.rules.boot_sanitation_rule import BootSanitationRule
from app.compliance.rules.hand_sanitation_rule import HandSanitationRule
from app.compliance.rules.uniform_rule import UniformRule
from app.compliance.rules.vehicle_sanitation_rule import VehicleSanitationRule
from app.compliance.rules.zone_intrusion_rule import ZoneIntrusionRule

RULE_CLASSES: list[type[BaseComplianceRule]] = [
    ZoneIntrusionRule,
    UniformRule,
    AnimalIntrusionRule,
    HandSanitationRule,
    BootSanitationRule,
    VehicleSanitationRule,
    BiosecurityProcessRule,
]


def load_compliance_rules() -> list[BaseComplianceRule]:
    return [rule_cls() for rule_cls in RULE_CLASSES]
