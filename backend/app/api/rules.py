from app.api.deps import get_current_user
import uuid
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.vi_catalog import CATEGORY_LABELS, SEVERITY_LABELS
from app.database.session import get_db
from app.models import BiosecurityRule
from app.schemas.biosecurity_rule import (
    BiosecurityRuleCreate,
    BiosecurityRuleResponse,
    BiosecurityRuleUpdate,
)
from app.schemas.event import EventEngineResponse
from app.schemas.zone_rule import ZoneRuleToggleResponse, ZoneRuleUpdate
from app.services.event_engine_service import event_to_engine_dict
from app.services.mock_rule_engine import trigger_rule
from app.services.zone_rule_service import (
    delete_zone_rule,
    get_zone_rule_or_none,
    rule_to_response_dict,
    toggle_zone_rule,
    update_zone_rule,
)

router = APIRouter(prefix="/rules", tags=["rules"], dependencies=[Depends(get_current_user)])

VN_TZ = timezone(timedelta(hours=7))


def _now_iso() -> str:
    return datetime.now(VN_TZ).isoformat()


def _bio_to_response(rule: BiosecurityRule) -> BiosecurityRuleResponse:
    return BiosecurityRuleResponse(
        id=rule.id,
        ma_quy_tac=rule.rule_code,
        ten_vi_pham=rule.rule_name_vi,
        nhom=CATEGORY_LABELS.get(rule.category, rule.category),
        muc_do=SEVERITY_LABELS.get(rule.severity, rule.severity),
        mo_ta=rule.description,
        kich_hoat=rule.enabled,
        thoi_gian_tao=rule.created_at,
    )


def _get_bio_rule_or_404(rule_id: str, db: Session) -> BiosecurityRule:
    rule = db.get(BiosecurityRule, rule_id)
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy quy tắc ATSH")
    return rule


def _infer_category(object_type: str) -> str:
    if object_type in {"dog", "cat", "rat", "bird"}:
        return "animal"
    if object_type == "vehicle":
        return "vehicle"
    if object_type == "person":
        return "human"
    return "movement"


def _is_zone_rule_id(rule_id: str) -> bool:
    return rule_id.startswith("ZR-")


@router.get("", response_model=list[BiosecurityRuleResponse])
def list_biosecurity_rules(db: Session = Depends(get_db)) -> list[BiosecurityRuleResponse]:
    rules = list(db.scalars(select(BiosecurityRule).order_by(BiosecurityRule.id)))
    return [_bio_to_response(rule) for rule in rules]


@router.post("", response_model=BiosecurityRuleResponse, status_code=status.HTTP_201_CREATED)
def create_biosecurity_rule(
    payload: BiosecurityRuleCreate,
    db: Session = Depends(get_db),
) -> BiosecurityRuleResponse:
    rule_id = payload.id or f"BR-{uuid.uuid4().hex[:8].upper()}"
    if db.get(BiosecurityRule, rule_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ID quy tắc đã tồn tại")

    object_type = (payload.object_type or "person").lower()
    rule = BiosecurityRule(
        id=rule_id,
        rule_code=payload.rule_code.upper(),
        rule_name_vi=payload.rule_name_vi,
        rule_name_en=payload.rule_name_en or payload.rule_name_vi,
        category=payload.category or _infer_category(object_type),
        severity=payload.severity.lower(),
        description=payload.description or payload.rule_name_vi,
        enabled=payload.enabled,
        created_at=_now_iso(),
        object_type=object_type,
        from_zone=payload.from_zone or "any_zone",
        to_zone=payload.to_zone or "any_zone",
        required_zone=payload.required_zone,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return _bio_to_response(rule)


@router.put("/{rule_id}")
def update_rule(rule_id: str, body: dict = Body(...), db: Session = Depends(get_db)):
    if _is_zone_rule_id(rule_id):
        zone_rule = get_zone_rule_or_none(db, rule_id)
        if zone_rule is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy rule")
        try:
            payload = ZoneRuleUpdate.model_validate(body)
            updated = update_zone_rule(db, zone_rule, payload)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
        return rule_to_response_dict(updated)

    rule = _get_bio_rule_or_404(rule_id, db)
    payload = BiosecurityRuleUpdate.model_validate(body)
    values = payload.model_dump(exclude_unset=True)
    if "severity" in values and values["severity"] is not None:
        values["severity"] = values["severity"].lower()
    if "rule_code" in values and values["rule_code"] is not None:
        values["rule_code"] = values["rule_code"].upper()
    if "object_type" in values and values["object_type"] is not None:
        values["object_type"] = values["object_type"].lower()

    for field, value in values.items():
        setattr(rule, field, value)

    db.add(rule)
    db.commit()
    db.refresh(rule)
    return _bio_to_response(rule)


@router.patch("/{rule_id}/toggle", response_model=ZoneRuleToggleResponse)
def toggle_rule(rule_id: str, db: Session = Depends(get_db)) -> ZoneRuleToggleResponse:
    zone_rule = get_zone_rule_or_none(db, rule_id)
    if zone_rule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy rule")
    updated = toggle_zone_rule(db, zone_rule)
    return ZoneRuleToggleResponse(id=updated.id, enabled=updated.enabled)


@router.post("/{rule_id}/trigger", response_model=EventEngineResponse)
def trigger_rule_endpoint(rule_id: str, db: Session = Depends(get_db)) -> EventEngineResponse:
    try:
        event = trigger_rule(db, rule_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return EventEngineResponse(**event_to_engine_dict(db, event))


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rule(rule_id: str, db: Session = Depends(get_db)) -> None:
    if _is_zone_rule_id(rule_id):
        zone_rule = get_zone_rule_or_none(db, rule_id)
        if zone_rule is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy rule")
        delete_zone_rule(db, zone_rule)
        return

    rule = _get_bio_rule_or_404(rule_id, db)
    db.delete(rule)
    db.commit()
