from __future__ import annotations

from dataclasses import dataclass, field

BIOSECURITY_PROCESS_VIOLATION = "BIOSECURITY_PROCESS_VIOLATION"

WORKFLOW_STEP_CODES = {
    "ENTER_SHOWER": "ENTER_SHOWER",
    "HAND_SANITIZATION": "HAND_SANITIZATION",
    "BOOT_SANITIZATION": "BOOT_SANITIZATION",
    "ENTER_CLEAN_ZONE": "ENTER_CLEAN_ZONE",
}

STEP_ZONE_CODES: dict[str, str] = {
    WORKFLOW_STEP_CODES["ENTER_SHOWER"]: "shower_room",
    WORKFLOW_STEP_CODES["HAND_SANITIZATION"]: "handwash_zone",
    WORKFLOW_STEP_CODES["BOOT_SANITIZATION"]: "boot_disinfection_tray",
}

CLEAN_PRODUCTION_ZONES = {
    "gestation_barn",
    "farrowing_barn",
    "weaning_barn",
    "nursery_barn",
    "boar_barn",
    "quarantine_barn",
}

STEP_LABELS_VI = {
    "ENTER_SHOWER": "Vào khu tắm",
    "HAND_SANITIZATION": "Sát trùng tay",
    "BOOT_SANITIZATION": "Sát trùng ủng",
    "ENTER_CLEAN_ZONE": "Vào vùng sạch",
}
