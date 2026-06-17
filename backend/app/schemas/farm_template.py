from typing import Optional

from pydantic import BaseModel, ConfigDict


class TemplateZoneDefinitionResponse(BaseModel):
    id: str
    template_id: str
    zone_code: str
    zone_name: str
    zone_category: str
    biosecurity_level: str
    risk_level: str
    color: str
    layout_x: float
    layout_y: float
    layout_w: float
    layout_h: float
    sort_order: int

    model_config = ConfigDict(from_attributes=True)


class FarmLayoutTemplateResponse(BaseModel):
    id: str
    name: str
    description: str
    version: str
    zones: list[TemplateZoneDefinitionResponse] = []

    model_config = ConfigDict(from_attributes=True)


class FarmLayoutTemplateSummaryResponse(BaseModel):
    id: str
    name: str
    description: str
    version: str
    zone_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class FarmZoneResponse(BaseModel):
    id: str
    farm_id: Optional[str]
    template_id: Optional[str]
    template_zone_id: Optional[str]
    zone_code: str
    name: str
    zone_category: str
    biosecurity_level: str
    risk_level: str
    layout_x: Optional[float]
    layout_y: Optional[float]
    layout_w: Optional[float]
    layout_h: Optional[float]
    sort_order: int
    active: bool

    model_config = ConfigDict(from_attributes=True)
