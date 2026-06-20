from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Camera, CameraZone, ZoneRule
from app.schemas.zone_rule import ZoneRuleCreate, ZoneRuleUpdate


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_zone_rule_id() -> str:
    return f"ZR-{uuid.uuid4().hex[:10].upper()}"


def rule_to_response_dict(rule: ZoneRule) -> dict:
    return {
        "id": rule.id,
        "camera_id": rule.camera_id,
        "zone_id": rule.zone_id,
        "name": rule.name,
        "description": rule.description,
        "rule_type": rule.rule_type,
        "severity": rule.severity,
        "enabled": rule.enabled,
        "cooldown_seconds": rule.cooldown_seconds,
        "config": rule.config or {},
        "created_at": rule.created_at,
        "updated_at": rule.updated_at,
    }


def _validate_zone(db: Session, camera_id: str, zone_id: str) -> CameraZone:
    zone = db.get(CameraZone, zone_id)
    if not zone or zone.camera_id != camera_id:
        raise ValueError("Zone không tồn tại hoặc không thuộc camera này")
    return zone


def list_rules_for_camera(db: Session, camera_id: str) -> list[ZoneRule]:
    return list(
        db.scalars(
            select(ZoneRule)
            .where(ZoneRule.camera_id == camera_id)
            .order_by(ZoneRule.created_at.desc(), ZoneRule.id)
        )
    )


def get_zone_rule_or_none(db: Session, rule_id: str) -> ZoneRule | None:
    return db.get(ZoneRule, rule_id)


def create_zone_rule(db: Session, camera_id: str, payload: ZoneRuleCreate) -> ZoneRule:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise ValueError("Không tìm thấy camera")

    _validate_zone(db, camera_id, payload.zone_id)

    now = utc_now_iso()
    rule = ZoneRule(
        id=new_zone_rule_id(),
        camera_id=camera_id,
        zone_id=payload.zone_id,
        name=payload.name,
        description=(payload.description or "").strip() or None,
        rule_type=payload.rule_type,
        severity=payload.severity,
        enabled=payload.enabled,
        cooldown_seconds=payload.cooldown_seconds,
        config=payload.config or {},
        created_at=now,
        updated_at=now,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def update_zone_rule(db: Session, rule: ZoneRule, payload: ZoneRuleUpdate) -> ZoneRule:
    values = payload.model_dump(exclude_unset=True)

    if "description" in values:
        values["description"] = (values["description"] or "").strip() or None

    if "zone_id" in values and values["zone_id"] is not None:
        _validate_zone(db, rule.camera_id, values["zone_id"])

    for field, value in values.items():
        setattr(rule, field, value)

    rule.updated_at = utc_now_iso()
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def toggle_zone_rule(db: Session, rule: ZoneRule) -> ZoneRule:
    rule.enabled = not rule.enabled
    rule.updated_at = utc_now_iso()
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def delete_zone_rule(db: Session, rule: ZoneRule) -> None:
    db.delete(rule)
    db.commit()
