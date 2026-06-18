"""Default ATSH workflow definitions for AMS v3.1."""

WORKFLOW_VIOLATION_CODES = {
    "KHONG_TAM_SAT_TRUNG": "Không tắm sát trùng",
    "KHONG_SAT_TRUNG_TAY": "Không sát trùng tay",
    "KHONG_SAT_TRUNG_UNG": "Không sát trùng ủng",
    "DI_SAI_QUY_TRINH": "Đi sai quy trình",
    "DI_NGUOC_TUYEN": "Đi ngược tuyến",
}

STANDARD_ENTRY_FLOW = [
    "worker_housing",
    "shower_room",
    "handwash_zone",
    "boot_disinfection_tray",
]

VIOLATION_CODE_BY_ZONE = {
    "shower_room": "KHONG_TAM_SAT_TRUNG",
    "handwash_zone": "KHONG_SAT_TRUNG_TAY",
    "boot_disinfection_tray": "KHONG_SAT_TRUNG_UNG",
}

COMMON_ENTRY_STEPS = [
    (1, "Nhà ở công nhân", "worker_housing"),
    (2, "Nhà tắm", "shower_room"),
    (3, "Sát trùng tay", "handwash_zone"),
    (4, "Sát trùng ủng", "boot_disinfection_tray"),
]

DEFAULT_WORKFLOWS = [
    {
        "id": "WF-GESTATION-ENTRY",
        "name": "Vào chuồng nái",
        "description": "Nhà ở công nhân → Nhà tắm → Sát trùng tay → Sát trùng ủng → Chuồng nái",
        "object_type": "person",
        "enabled": True,
        "final_step": ("Chuồng nái", "gestation_barn"),
    },
    {
        "id": "WF-FARROWING-ENTRY",
        "name": "Vào chuồng đẻ",
        "description": "Nhà ở công nhân → Nhà tắm → Sát trùng tay → Sát trùng ủng → Chuồng đẻ",
        "object_type": "person",
        "enabled": True,
        "final_step": ("Chuồng đẻ", "farrowing_barn"),
    },
    {
        "id": "WF-BOAR-ENTRY",
        "name": "Vào chuồng đực giống",
        "description": "Nhà ở công nhân → Nhà tắm → Sát trùng tay → Sát trùng ủng → Chuồng đực giống",
        "object_type": "person",
        "enabled": True,
        "final_step": ("Chuồng đực giống", "boar_barn"),
    },
]


def build_workflow_steps(workflow_id: str, final_step: tuple[str, str]) -> list[tuple[str, int, str, str]]:
    prefix = workflow_id.replace("WF-", "")
    steps = [
        (f"WFS-{prefix}-{order:02d}", order, name, zone_code)
        for order, name, zone_code in COMMON_ENTRY_STEPS
    ]
    final_name, final_zone = final_step
    steps.append((f"WFS-{prefix}-05", 5, final_name, final_zone))
    return steps


DEFAULT_PERSON_ENTRY_WORKFLOW = {
    **DEFAULT_WORKFLOWS[0],
    "steps": build_workflow_steps(DEFAULT_WORKFLOWS[0]["id"], DEFAULT_WORKFLOWS[0]["final_step"]),
}
