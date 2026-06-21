from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class EventResponse(BaseModel):
    id: str
    ten_vi_pham: str
    muc_do: str
    ten_vung: str
    ten_camera: str
    ten_trang_trai: str
    do_tin_cay: int
    thoi_gian: str
    trang_thai: str
    nguoi_xu_ly: str
    event_type: Optional[str] = None
    camera_id: Optional[str] = None
    zone_id: Optional[str] = None
    rule_id: Optional[str] = None
    rule_name: Optional[str] = None
    snapshot_path: Optional[str] = None
    score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class EventEngineResponse(BaseModel):
    id: str
    camera_id: str
    zone_id: Optional[str]
    rule_id: Optional[str]
    rule_name: Optional[str]
    event_type: Optional[str]
    confidence: Optional[float]
    score: Optional[float] = None
    snapshot_url: Optional[str]
    snapshotPath: Optional[str] = None
    ruleId: Optional[str] = None
    ruleName: Optional[str] = None
    started_at: Optional[str]
    ended_at: Optional[str]
    status: str
    metadata: Optional[dict[str, Any]] = Field(default=None, alias="event_metadata")
    created_at: Optional[str] = Field(default=None, alias="record_created_at")
    camera_name: Optional[str] = None
    zone_name: Optional[str] = None
    severity: Optional[str] = None
    severityLabel: Optional[str] = None
    classification: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    recommendedAction: Optional[str] = None
    explanation: Optional[dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PaginatedEventsResponse(BaseModel):
    items: list[EventEngineResponse]
    total: int
    page: int
    limit: int


class EmailAlertPreview(BaseModel):
    tieu_de: str
    noi_dung: str
