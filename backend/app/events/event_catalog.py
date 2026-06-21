from __future__ import annotations

from dataclasses import dataclass
from typing import Any

EVENT_CLASSIFICATIONS = ("BIOSECURITY", "ANIMAL", "VEHICLE", "SYSTEM")
EVENT_SEVERITIES = ("LOW", "MEDIUM", "HIGH", "CRITICAL")

EVENT_TYPE_ALIASES = {
    "PROCESS_VIOLATION": "BIOSECURITY_PROCESS_VIOLATION",
}


@dataclass(frozen=True)
class EventExplanation:
    title: str
    description: str
    recommended_action: str

    def to_dict(self) -> dict[str, str]:
        return {
            "title": self.title,
            "description": self.description,
            "recommendedAction": self.recommended_action,
        }


@dataclass(frozen=True)
class EventCatalogEntry:
    classification: str
    severity: str
    explanation: EventExplanation


EVENT_CATALOG: dict[str, EventCatalogEntry] = {
    "UNIFORM_VIOLATION": EventCatalogEntry(
        classification="BIOSECURITY",
        severity="MEDIUM",
        explanation=EventExplanation(
            title="Sai đồng phục vùng",
            description="Người đi vào vùng sạch nhưng không sử dụng đồng phục phù hợp.",
            recommended_action="Kiểm tra quy trình thay đồ và sát trùng.",
        ),
    ),
    "NO_HAND_SANITIZATION": EventCatalogEntry(
        classification="BIOSECURITY",
        severity="HIGH",
        explanation=EventExplanation(
            title="Không sát trùng tay",
            description="Người bỏ qua bước rửa tay sát trùng trước khi vào vùng kiểm soát.",
            recommended_action="Nhắc nhở và kiểm tra lại quy trình sát trùng tay tại điểm giám sát.",
        ),
    ),
    "NO_BOOT_SANITIZATION": EventCatalogEntry(
        classification="BIOSECURITY",
        severity="HIGH",
        explanation=EventExplanation(
            title="Không sát trùng ủng",
            description="Người bỏ qua bước sát trùng ủng trước khi vào vùng sạch.",
            recommended_action="Kiểm tra khay sát trùng ủng và giám sát tuân thủ quy trình.",
        ),
    ),
    "ZONE_INTRUSION": EventCatalogEntry(
        classification="BIOSECURITY",
        severity="HIGH",
        explanation=EventExplanation(
            title="Xâm nhập vùng cấm",
            description="Người hoặc đối tượng đi vào vùng bị hạn chế hoặc cấm tuyệt đối.",
            recommended_action="Xác minh danh tính, ghi nhận vi phạm và áp dụng biện pháp cách ly.",
        ),
    ),
    "BIOSECURITY_PROCESS_VIOLATION": EventCatalogEntry(
        classification="BIOSECURITY",
        severity="CRITICAL",
        explanation=EventExplanation(
            title="Vi phạm quy trình an toàn sinh học",
            description="Người bỏ qua một hoặc nhiều bước bắt buộc trong quy trình vào vùng sạch.",
            recommended_action="Dừng di chuyển, đưa người vi phạm quay lại thực hiện đầy đủ quy trình.",
        ),
    ),
    "ANIMAL_INTRUSION": EventCatalogEntry(
        classification="ANIMAL",
        severity="HIGH",
        explanation=EventExplanation(
            title="Động vật xâm nhập",
            description="Động vật không được phép xuất hiện trong vùng sản xuất hoặc vùng sạch.",
            recommended_action="Loại bỏ động vật khỏi vùng và kiểm tra rào chắn, cửa ra vào.",
        ),
    ),
    "VEHICLE_INTRUSION": EventCatalogEntry(
        classification="VEHICLE",
        severity="HIGH",
        explanation=EventExplanation(
            title="Xe vi phạm sát trùng",
            description="Phương tiện vào vùng kiểm soát mà chưa hoàn thành quy trình sát trùng.",
            recommended_action="Dừng xe, yêu cầu sát trùng lại và ghi nhận biển số.",
        ),
    ),
    "CAMERA_OFFLINE": EventCatalogEntry(
        classification="SYSTEM",
        severity="MEDIUM",
        explanation=EventExplanation(
            title="Camera mất kết nối",
            description="Camera không gửi tín hiệu hoặc heartbeat trong thời gian quy định.",
            recommended_action="Kiểm tra nguồn điện, mạng và thiết bị tại vị trí camera.",
        ),
    ),
}

CATEGORY_CLASSIFICATION_MAP = {
    "compliance_violation": "BIOSECURITY",
    "animal_intrusion": "ANIMAL",
    "atsh_violation": "BIOSECURITY",
    "workflow_violation": "BIOSECURITY",
    "camera_offline": "SYSTEM",
    "rule_engine": "BIOSECURITY",
}


def normalize_event_type(event_type: str | None) -> str | None:
    if not event_type:
        return None
    normalized = str(event_type).strip().upper()
    return EVENT_TYPE_ALIASES.get(normalized, normalized)


def resolve_event_classification(
    event_type: str | None,
    *,
    category: str | None = None,
) -> str:
    normalized = normalize_event_type(event_type)
    if normalized and normalized in EVENT_CATALOG:
        return EVENT_CATALOG[normalized].classification
    if category and category in CATEGORY_CLASSIFICATION_MAP:
        return CATEGORY_CLASSIFICATION_MAP[category]
    return "SYSTEM"


def resolve_event_severity(
    event_type: str | None,
    *,
    fallback: str | None = None,
) -> str:
    normalized = normalize_event_type(event_type)
    if normalized and normalized in EVENT_CATALOG:
        return EVENT_CATALOG[normalized].severity
    if fallback:
        upper = str(fallback).upper()
        if upper in EVENT_SEVERITIES:
            return upper
        legacy_map = {
            "CRITICAL": "CRITICAL",
            "DANGER": "CRITICAL",
            "HIGH": "HIGH",
            "WARNING": "MEDIUM",
            "MEDIUM": "MEDIUM",
            "LOW": "LOW",
            "INFO": "LOW",
        }
        return legacy_map.get(upper, "MEDIUM")
    return "MEDIUM"


def build_event_explanation(
    event_type: str | None,
    *,
    rule_name: str | None = None,
    zone_name: str | None = None,
) -> dict[str, str]:
    normalized = normalize_event_type(event_type)
    entry = EVENT_CATALOG.get(normalized or "")
    if entry:
        explanation = entry.explanation.to_dict()
        if rule_name and normalized == "BIOSECURITY_PROCESS_VIOLATION":
            explanation["title"] = rule_name
        if zone_name:
            explanation["description"] = f"{explanation['description']} Vùng: {zone_name}."
        return explanation

    title = rule_name or normalized or "Vi phạm tuân thủ"
    return {
        "title": title,
        "description": f"Sự kiện {title} được ghi nhận bởi hệ thống AMS.",
        "recommendedAction": "Kiểm tra camera, xác minh vi phạm và xử lý theo quy trình nội bộ.",
    }


def enrich_event_fields(
    *,
    event_type: str | None,
    category: str | None = None,
    severity: str | None = None,
    rule_name: str | None = None,
    zone_name: str | None = None,
) -> dict[str, Any]:
    normalized_type = normalize_event_type(event_type)
    resolved_severity = resolve_event_severity(normalized_type, fallback=severity)
    classification = resolve_event_classification(normalized_type, category=category)
    explanation = build_event_explanation(
        normalized_type,
        rule_name=rule_name,
        zone_name=zone_name,
    )
    return {
        "event_type": normalized_type or event_type,
        "classification": classification,
        "severity": resolved_severity,
        "title": explanation["title"],
        "description": explanation["description"],
        "recommendedAction": explanation["recommendedAction"],
        "explanation": explanation,
    }
