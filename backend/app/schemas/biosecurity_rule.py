from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BiosecurityRuleBase(BaseModel):
    rule_code: str = Field(min_length=1, max_length=80)
    rule_name_vi: str = Field(min_length=1, max_length=160)
    category: str = Field(min_length=1, max_length=40)
    severity: str = Field(min_length=1, max_length=20)
    description: str = ""
    enabled: bool = True
    object_type: Optional[str] = None
    from_zone: Optional[str] = None
    to_zone: Optional[str] = None
    required_zone: Optional[str] = None


class BiosecurityRuleCreate(BiosecurityRuleBase):
    id: Optional[str] = None
    rule_name_en: Optional[str] = None


class BiosecurityRuleUpdate(BaseModel):
    rule_code: Optional[str] = None
    rule_name_vi: Optional[str] = None
    rule_name_en: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    object_type: Optional[str] = None
    from_zone: Optional[str] = None
    to_zone: Optional[str] = None
    required_zone: Optional[str] = None


class BiosecurityRuleResponse(BaseModel):
    id: str
    ma_quy_tac: str
    ten_vi_pham: str
    nhom: str
    muc_do: str
    mo_ta: str
    kich_hoat: bool
    thoi_gian_tao: str

    model_config = ConfigDict(from_attributes=True)


class BiosecurityCategoryResponse(BaseModel):
    ma: str
    ten: str
