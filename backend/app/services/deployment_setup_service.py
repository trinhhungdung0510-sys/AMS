from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.compliance.constants import COMPLIANCE_RULE_DEFINITIONS, COMPLIANCE_RULE_IDS
from app.compliance.uniform_matcher import match_uniform
from app.events.event_catalog import build_event_explanation, resolve_event_severity
from app.models import Camera, CameraZone, Farm, UniformTemplate
from app.services.deployment_health_service import build_health_report
from app.services.camera_zone_service import get_camera_zone_or_none, zone_to_response_dict
from app.services.system_settings_service import get_system_settings


def get_setup_status(db: Session) -> dict[str, Any]:
    farm_count = db.scalar(select(func.count()).select_from(Farm)) or 0
    camera_count = db.scalar(select(func.count()).select_from(Camera)) or 0
    zone_count = db.scalar(select(func.count()).select_from(CameraZone)) or 0
    uniform_count = db.scalar(select(func.count()).select_from(UniformTemplate)) or 0

    steps = {
        "farm": {"completed": farm_count > 0, "count": farm_count},
        "camera": {"completed": camera_count > 0, "count": camera_count},
        "zone": {"completed": zone_count > 0, "count": zone_count},
        "uniform": {"completed": uniform_count > 0, "count": uniform_count},
        "systemCheck": {"completed": False, "count": 0},
    }

    health = build_health_report(db)
    steps["systemCheck"]["completed"] = health["status"] in {"ok", "degraded"}
    steps["systemCheck"]["status"] = health["status"]

    completed = all(step["completed"] for step in steps.values())
    return {
        "completed": completed,
        "steps": steps,
        "health": health,
    }


def test_zone(db: Session, zone_id: str) -> dict[str, Any]:
    zone = get_camera_zone_or_none(db, zone_id)
    if zone is None:
        from app.models import ZonePolygon

        polygon = db.get(ZonePolygon, zone_id)
        if polygon is None:
            raise ValueError("Không tìm thấy zone")
        return {
            "zoneId": polygon.id,
            "zoneName": polygon.zone_name,
            "zoneType": polygon.zone_type,
            "farmId": polygon.farm_id,
            "cameraId": polygon.camera_id,
            "overlay": {
                "points": polygon.polygon_points,
                "color": polygon.color,
                "opacity": polygon.opacity,
            },
            "coordinates": polygon.polygon_points,
        }

    camera = db.get(Camera, zone.camera_id)
    payload = zone_to_response_dict(zone)
    return {
        "zoneId": zone.id,
        "zoneName": zone.name,
        "zoneType": zone.zone_type,
        "farmId": zone.farm_id,
        "cameraId": zone.camera_id,
        "cameraName": camera.name if camera else zone.camera_id,
        "overlay": {
            "points": payload["points"],
            "color": payload["color"],
            "referenceWidth": payload.get("reference_width"),
            "referenceHeight": payload.get("reference_height"),
        },
        "coordinates": payload["points"],
    }


def test_compliance_rule(
    db: Session,
    *,
    rule_type: str,
    track_id: int | None = None,
    camera_id: str | None = None,
    zone_id: str | None = None,
    score_input: float | None = None,
) -> dict[str, Any]:
    normalized = rule_type.upper()
    if normalized not in COMPLIANCE_RULE_IDS.values():
        raise ValueError(f"Rule không hỗ trợ: {rule_type}")

    settings = get_system_settings(db)
    threshold = float(settings.get("compliance_threshold", 0.85))
    explanation = build_event_explanation(normalized)

    rule_input = {
        "ruleType": normalized,
        "trackId": track_id,
        "cameraId": camera_id,
        "zoneId": zone_id,
        "threshold": threshold,
    }

    if normalized == COMPLIANCE_RULE_IDS["UNIFORM_VIOLATION"]:
        match = match_uniform(b"mock-image", ["template-a.jpg"], track_id=track_id or 1, threshold=threshold)
        violated = not match.matched
        score = score_input if score_input is not None else match.score
        output = {
            "violated": violated,
            "score": score,
            "matched": match.matched,
            "severity": resolve_event_severity(normalized, fallback="MEDIUM" if violated else "LOW"),
            "title": explanation["title"],
            "description": explanation["description"],
            "recommendedAction": explanation["recommendedAction"],
        }
    else:
        simulated_score = score_input if score_input is not None else 0.42
        violated = simulated_score < threshold
        output = {
            "violated": violated,
            "score": simulated_score,
            "severity": resolve_event_severity(normalized),
            "title": explanation["title"],
            "description": explanation["description"],
            "recommendedAction": explanation["recommendedAction"],
            "note": "Simulation mode — no new detector invoked",
        }

    rule_def = next((item for item in COMPLIANCE_RULE_DEFINITIONS if item.event_type == normalized), None)
    return {
        "rule": {
            "id": normalized,
            "name": rule_def.name if rule_def else normalized,
            "description": rule_def.description if rule_def else "",
        },
        "input": rule_input,
        "output": output,
    }
