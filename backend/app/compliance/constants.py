from __future__ import annotations

from dataclasses import dataclass

COMPLIANCE_RULE_IDS = {
    "ZONE_INTRUSION": "ZONE_INTRUSION",
    "NO_HAND_SANITIZATION": "NO_HAND_SANITIZATION",
    "NO_BOOT_SANITIZATION": "NO_BOOT_SANITIZATION",
    "ANIMAL_INTRUSION": "ANIMAL_INTRUSION",
    "VEHICLE_INTRUSION": "VEHICLE_INTRUSION",
    "UNIFORM_VIOLATION": "UNIFORM_VIOLATION",
    "BIOSECURITY_PROCESS_VIOLATION": "BIOSECURITY_PROCESS_VIOLATION",
}


@dataclass(frozen=True)
class ComplianceRuleDefinition:
    id: str
    name: str
    event_type: str
    description: str


COMPLIANCE_RULE_DEFINITIONS: tuple[ComplianceRuleDefinition, ...] = (
    ComplianceRuleDefinition(
        id=COMPLIANCE_RULE_IDS["ZONE_INTRUSION"],
        name="Xâm nhập vùng cấm",
        event_type="ZONE_INTRUSION",
        description="Person enters restricted biosecurity zone without authorization.",
    ),
    ComplianceRuleDefinition(
        id=COMPLIANCE_RULE_IDS["NO_HAND_SANITIZATION"],
        name="Không rửa tay sát trùng",
        event_type="NO_HAND_SANITIZATION",
        description="Person skips mandatory hand sanitation step.",
    ),
    ComplianceRuleDefinition(
        id=COMPLIANCE_RULE_IDS["NO_BOOT_SANITIZATION"],
        name="Không sát trùng ủng",
        event_type="NO_BOOT_SANITIZATION",
        description="Person skips mandatory boot disinfection step.",
    ),
    ComplianceRuleDefinition(
        id=COMPLIANCE_RULE_IDS["ANIMAL_INTRUSION"],
        name="Động vật xâm nhập",
        event_type="ANIMAL_INTRUSION",
        description="Unauthorized animal enters restricted production zone.",
    ),
    ComplianceRuleDefinition(
        id=COMPLIANCE_RULE_IDS["VEHICLE_INTRUSION"],
        name="Xe xâm nhập / chưa sát trùng",
        event_type="VEHICLE_INTRUSION",
        description="Vehicle enters zone without required disinfection workflow.",
    ),
    ComplianceRuleDefinition(
        id=COMPLIANCE_RULE_IDS["UNIFORM_VIOLATION"],
        name="Sai đồng phục bảo hộ",
        event_type="UNIFORM_VIOLATION",
        description="Person wears wrong protective uniform for the zone.",
    ),
    ComplianceRuleDefinition(
        id=COMPLIANCE_RULE_IDS["BIOSECURITY_PROCESS_VIOLATION"],
        name="Vi phạm quy trình an toàn sinh học",
        event_type="BIOSECURITY_PROCESS_VIOLATION",
        description="Person skips mandatory biosecurity workflow steps.",
    ),
)
