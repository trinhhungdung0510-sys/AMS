from app.api.deps import get_current_user
import uuid
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.biosecurity_ai_v40 import FARM_AREA_TYPES, normalize_atsh_severity
from app.data.vi_catalog import CATEGORY_LABELS, SEVERITY_LABELS
from app.database.session import get_db
from app.models import BiosecurityRule
from app.schemas.biosecurity_rule import (
    BiosecurityCategoryResponse,
    BiosecurityRuleCreate,
    BiosecurityRuleResponse,
    BiosecurityRuleUpdate,
    FarmAreaTypeResponse,
)

router = APIRouter(prefix="/biosecurity-rules", tags=["biosecurity-rules"],
    dependencies=[Depends(get_current_user)]
)

VN_TZ = timezone(timedelta(hours=7))


def _now_iso() -> str:
    return datetime.now(VN_TZ).isoformat()


def _to_response(rule: BiosecurityRule) -> BiosecurityRuleResponse:
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


def _get_rule_or_404(rule_id: str, db: Session) -> BiosecurityRule:
    rule = db.get(BiosecurityRule, rule_id)
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy quy tắc ATSH")
    return rule


def _validate_category(category: str) -> None:
    if category not in CATEGORY_LABELS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Nhóm quy tắc không hợp lệ: {category}",
        )


def _validate_severity(severity: str) -> None:
    normalized = normalize_atsh_severity(severity)
    if normalized not in {"INFO", "WARNING", "CRITICAL"} and severity.lower() not in SEVERITY_LABELS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Mức độ cảnh báo không hợp lệ: {severity}",
        )


@router.get("/farm-areas", response_model=list[FarmAreaTypeResponse])
def list_farm_area_types() -> list[FarmAreaTypeResponse]:
    return [
        FarmAreaTypeResponse(
            ma_vung=code,
            ten_vi=ten_vi,
            ten_en=ten_en,
            muc_atsh=muc,
        )
        for code, ten_vi, ten_en, muc in FARM_AREA_TYPES
    ]


@router.get("/categories", response_model=list[BiosecurityCategoryResponse])
def list_categories() -> list[BiosecurityCategoryResponse]:
    return [BiosecurityCategoryResponse(ma=code, ten=label) for code, label in CATEGORY_LABELS.items()]


@router.get("/enabled", response_model=list[BiosecurityRuleResponse])
def list_enabled_rules(db: Session = Depends(get_db)) -> list[BiosecurityRuleResponse]:
    rules = list(
        db.scalars(
            select(BiosecurityRule)
            .where(BiosecurityRule.enabled.is_(True))
            .order_by(BiosecurityRule.category, BiosecurityRule.rule_code)
        )
    )
    return [_to_response(rule) for rule in rules]


@router.get("", response_model=list[BiosecurityRuleResponse])
def list_rules(db: Session = Depends(get_db)) -> list[BiosecurityRuleResponse]:
    rules = list(
        db.scalars(select(BiosecurityRule).order_by(BiosecurityRule.category, BiosecurityRule.rule_code))
    )
    return [_to_response(rule) for rule in rules]


@router.get("/{rule_id}", response_model=BiosecurityRuleResponse)
def get_rule(rule_id: str, db: Session = Depends(get_db)) -> BiosecurityRuleResponse:
    return _to_response(_get_rule_or_404(rule_id, db))


@router.post("", response_model=BiosecurityRuleResponse, status_code=status.HTTP_201_CREATED)
def create_rule(payload: BiosecurityRuleCreate, db: Session = Depends(get_db)) -> BiosecurityRuleResponse:
    _validate_category(payload.category)
    _validate_severity(payload.severity)

    rule_id = payload.id or f"BR-{uuid.uuid4().hex[:8].upper()}"
    if db.get(BiosecurityRule, rule_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ID quy tắc đã tồn tại")

    existing_code = db.scalar(
        select(BiosecurityRule.id).where(BiosecurityRule.rule_code == payload.rule_code.upper()).limit(1)
    )
    if existing_code:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mã quy tắc đã tồn tại")

    rule = BiosecurityRule(
        id=rule_id,
        rule_code=payload.rule_code.upper(),
        rule_name_vi=payload.rule_name_vi,
        rule_name_en=payload.rule_name_en or payload.rule_name_vi,
        category=payload.category,
        severity=normalize_atsh_severity(payload.severity).lower(),
        description=payload.description,
        enabled=payload.enabled,
        created_at=_now_iso(),
        object_type=payload.object_type.lower() if payload.object_type else "catalog",
        from_zone=payload.from_zone,
        to_zone=payload.to_zone,
        required_zone=payload.required_zone,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return _to_response(rule)


@router.put("/{rule_id}", response_model=BiosecurityRuleResponse)
def update_rule(
    rule_id: str,
    payload: BiosecurityRuleUpdate,
    db: Session = Depends(get_db),
) -> BiosecurityRuleResponse:
    rule = _get_rule_or_404(rule_id, db)
    values = payload.model_dump(exclude_unset=True)

    if "category" in values and values["category"] is not None:
        _validate_category(values["category"])
    if "severity" in values and values["severity"] is not None:
        _validate_severity(values["severity"])
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
    return _to_response(rule)


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rule(rule_id: str, db: Session = Depends(get_db)) -> None:
    rule = _get_rule_or_404(rule_id, db)
    db.delete(rule)
    db.commit()
