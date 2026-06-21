from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.events.event_catalog import (
    build_event_explanation,
    normalize_event_type,
    resolve_event_classification,
    resolve_event_severity,
)
from app.models import Event
from app.services.event_query_service import query_events_all
from app.services.vi_localization import resolve_camera_name, resolve_zone_name

COMPLIANCE_EVENT_TYPES = set(COMPLIANCE_RULE_IDS.values())
MONITORED_EVENT_TYPES = COMPLIANCE_EVENT_TYPES | {"CAMERA_OFFLINE"}

SEVERITY_PENALTY = {
    "CRITICAL": 10,
    "critical": 10,
    "HIGH": 5,
    "high": 5,
    "danger": 5,
    "MEDIUM": 2,
    "medium": 2,
    "warning": 2,
    "LOW": 1,
    "low": 1,
    "info": 1,
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def today_key() -> str:
    return utc_now().date().isoformat()


def since_days_iso(days: int) -> str:
    return (utc_now() - timedelta(days=days)).isoformat()


def _load_events(
    db: Session,
    *,
    days: int | None = None,
    date_prefix: str | None = None,
) -> list[Event]:
    since_iso = since_days_iso(days) if days else None
    return query_events_all(
        db,
        event_types=MONITORED_EVENT_TYPES,
        date_prefix=date_prefix,
        since_iso=since_iso if not date_prefix else None,
    )


def _compliance_score(events: list[Event]) -> int:
    penalty = 0
    for event in events:
        event_type = normalize_event_type(event.event_type)
        severity = resolve_event_severity(event_type, fallback=event.severity)
        penalty += SEVERITY_PENALTY.get(severity, 1)
    return max(0, min(100, 100 - penalty))


def _count_by_classification(events: list[Event]) -> dict[str, int]:
    counts = {"BIOSECURITY": 0, "ANIMAL": 0, "VEHICLE": 0, "SYSTEM": 0}
    for event in events:
        classification = resolve_event_classification(
            event.event_type,
            category=event.category,
        )
        counts[classification] = counts.get(classification, 0) + 1
    return counts


def build_period_summary(db: Session, *, days: int | None = None, date_prefix: str | None = None) -> dict:
    events = _load_events(db, days=days, date_prefix=date_prefix)
    by_class = _count_by_classification(events)
    by_type = Counter(normalize_event_type(event.event_type) or "UNKNOWN" for event in events)
    by_severity = Counter(
        resolve_event_severity(event.event_type, fallback=event.severity) for event in events
    )

    return {
        "totalViolations": len(events),
        "complianceScore": _compliance_score(events),
        "biosecurityViolations": by_class["BIOSECURITY"],
        "animalViolations": by_class["ANIMAL"],
        "vehicleViolations": by_class["VEHICLE"],
        "systemViolations": by_class["SYSTEM"],
        "byEventType": dict(by_type),
        "bySeverity": dict(by_severity),
    }


def build_dashboard_kpis(db: Session) -> dict:
    today = today_key()
    today_events = _load_events(db, date_prefix=today)
    by_class = _count_by_classification(today_events)
    compliance_score = _compliance_score(today_events)

    try:
        from app.services.demo_mode_service import is_demo_mode
        from app.services.demo_event_generator import demo_event_generator

        if is_demo_mode(db) and demo_event_generator.is_running:
            compliance_score = demo_event_generator.current_compliance_score()
    except Exception:
        pass

    return {
        "date": today,
        "totalViolationsToday": len(today_events),
        "biosecurityViolations": by_class["BIOSECURITY"],
        "animalViolations": by_class["ANIMAL"],
        "vehicleViolations": by_class["VEHICLE"],
        "complianceScore": compliance_score,
    }


def build_top_violations(db: Session, *, days: int = 7, limit: int = 10) -> list[dict]:
    events = _load_events(db, days=days)
    grouped: dict[str, dict] = defaultdict(lambda: {"count": 0, "severity": "MEDIUM", "classification": "BIOSECURITY"})

    for event in events:
        event_type = normalize_event_type(event.event_type) or "UNKNOWN"
        grouped[event_type]["count"] += 1
        grouped[event_type]["severity"] = resolve_event_severity(event_type, fallback=event.severity)
        grouped[event_type]["classification"] = resolve_event_classification(
            event_type,
            category=event.category,
        )
        grouped[event_type]["title"] = build_event_explanation(
            event_type,
            rule_name=event.alert_type,
        )["title"]

    ranked = sorted(grouped.items(), key=lambda item: item[1]["count"], reverse=True)[:limit]
    return [
        {
            "eventType": event_type,
            "title": stats.get("title") or event_type,
            "count": stats["count"],
            "severity": stats["severity"],
            "classification": stats["classification"],
        }
        for event_type, stats in ranked
    ]


def build_pdf_report_structure(db: Session, *, days: int = 30) -> dict:
    events = _load_events(db, days=days)
    summary = build_period_summary(db, days=days)

    violations = []
    for event in events[:50]:
        event_type = normalize_event_type(event.event_type)
        explanation = build_event_explanation(
            event_type,
            rule_name=event.alert_type,
            zone_name=resolve_zone_name(db, event.zone),
        )
        violations.append(
            {
                "id": event.id,
                "eventType": event_type,
                "classification": resolve_event_classification(event_type, category=event.category),
                "severity": resolve_event_severity(event_type, fallback=event.severity),
                "cameraId": event.camera_id,
                "cameraName": resolve_camera_name(db, event.camera_id),
                "zoneName": resolve_zone_name(db, event.zone),
                "occurredAt": event.occurred_at,
                "title": explanation["title"],
                "description": explanation["description"],
                "recommendedAction": explanation["recommendedAction"],
            }
        )

    zone_counts = Counter(resolve_zone_name(db, event.zone) for event in events)
    rule_counts = Counter(
        build_event_explanation(
            normalize_event_type(event.event_type),
            rule_name=event.alert_type,
        )["title"]
        for event in events
    )

    return {
        "summary": summary,
        "violations": violations,
        "topZones": [
            {"zoneName": zone, "count": count}
            for zone, count in zone_counts.most_common(10)
        ],
        "topRules": [
            {"ruleName": rule, "count": count}
            for rule, count in rule_counts.most_common(10)
        ],
    }


def build_compliance_report(db: Session) -> dict:
    return {
        "today": build_period_summary(db, date_prefix=today_key()),
        "sevenDays": build_period_summary(db, days=7),
        "thirtyDays": build_period_summary(db, days=30),
        "kpis": build_dashboard_kpis(db),
        "topViolations7Days": build_top_violations(db, days=7, limit=10),
    }
