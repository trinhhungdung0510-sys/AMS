from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.zone_rule import RULE_SEVERITIES, RULE_TYPES


class ZoneRuleCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    zone_id: str = Field(min_length=1, max_length=24)
    description: Optional[str] = Field(default=None, max_length=500)
    rule_type: str = Field(max_length=40)
    severity: str = Field(default="MEDIUM", max_length=20)
    enabled: bool = Field(default=True)
    cooldown_seconds: int = Field(default=60, ge=0, le=86400)
    config: dict[str, Any] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Tên rule không được để trống")
        return cleaned

    @field_validator("rule_type")
    @classmethod
    def validate_rule_type(cls, value: str) -> str:
        cleaned = value.strip().upper()
        if cleaned not in RULE_TYPES:
            allowed = ", ".join(sorted(RULE_TYPES))
            raise ValueError(f"rule_type phải là một trong: {allowed}")
        return cleaned

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, value: str) -> str:
        cleaned = value.strip().upper()
        if cleaned not in RULE_SEVERITIES:
            allowed = ", ".join(sorted(RULE_SEVERITIES))
            raise ValueError(f"severity phải là một trong: {allowed}")
        return cleaned


class ZoneRuleUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    zone_id: Optional[str] = Field(default=None, max_length=24)
    description: Optional[str] = Field(default=None, max_length=500)
    rule_type: Optional[str] = Field(default=None, max_length=40)
    severity: Optional[str] = Field(default=None, max_length=20)
    enabled: Optional[bool] = None
    cooldown_seconds: Optional[int] = Field(default=None, ge=0, le=86400)
    config: Optional[dict[str, Any]] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Tên rule không được để trống")
        return cleaned

    @field_validator("rule_type")
    @classmethod
    def validate_rule_type(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        cleaned = value.strip().upper()
        if cleaned not in RULE_TYPES:
            allowed = ", ".join(sorted(RULE_TYPES))
            raise ValueError(f"rule_type phải là một trong: {allowed}")
        return cleaned

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        cleaned = value.strip().upper()
        if cleaned not in RULE_SEVERITIES:
            allowed = ", ".join(sorted(RULE_SEVERITIES))
            raise ValueError(f"severity phải là một trong: {allowed}")
        return cleaned


class ZoneRuleResponse(BaseModel):
    id: str
    camera_id: str
    zone_id: str
    name: str
    description: Optional[str]
    rule_type: str
    severity: str
    enabled: bool
    cooldown_seconds: int
    config: dict[str, Any]
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class ZoneRuleToggleResponse(BaseModel):
    id: str
    enabled: bool
