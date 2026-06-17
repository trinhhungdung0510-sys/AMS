from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class WorkflowStepBase(BaseModel):
    step_order: int = Field(ge=1)
    step_name: str = Field(min_length=2, max_length=120)
    zone_code: str = Field(min_length=2, max_length=40)
    required: bool = True


class WorkflowStepResponse(WorkflowStepBase):
    id: str
    workflow_id: str
    thu_tu: int
    zone_type: str
    ten_buoc: str
    bat_buoc: bool

    model_config = ConfigDict(from_attributes=True)


class WorkflowBase(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    description: str = Field(min_length=2)
    object_type: str = Field(min_length=2, max_length=40)
    enabled: bool = True


class WorkflowCreate(WorkflowBase):
    id: Optional[str] = None
    steps: list[WorkflowStepBase] = Field(min_length=1)


class WorkflowUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=160)
    description: Optional[str] = None
    object_type: Optional[str] = Field(default=None, min_length=2, max_length=40)
    enabled: Optional[bool] = None
    steps: Optional[list[WorkflowStepBase]] = None


class WorkflowResponse(WorkflowBase):
    id: str
    created_at: str
    ten_quy_trinh: str
    mo_ta: str
    kich_hoat: bool
    steps: list[WorkflowStepResponse] = []

    model_config = ConfigDict(from_attributes=True)


class WorkflowComplianceSummary(BaseModel):
    workflow_id: str
    workflow_name: str
    ten_quy_trinh: str
    compliance_score: int
    total_tracks: int
    compliant_tracks: int
    violation_count: int
    vi_pham_hom_nay: int
    top_quy_trinh_bi_vi_pham: list[dict]
    expected_steps: list[str]
    recent_violations: list[dict]


class WorkflowHistoryItem(BaseModel):
    event_id: str
    workflow_id: Optional[str] = None
    ten_quy_trinh: Optional[str] = None
    track_id: Optional[int] = None
    loai_vi_pham: Optional[str] = None
    ten_vi_pham: str
    ten_vung: str
    muc_do: str
    thoi_gian: str
    cac_vung_da_di: list[dict] = []
    camera_id: str


class WorkflowDashboardResponse(BaseModel):
    vi_pham_hom_nay: int
    top_quy_trinh_bi_vi_pham: list[dict]
    chi_tiet_hom_nay: list[dict]
