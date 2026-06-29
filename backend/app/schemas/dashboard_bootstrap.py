from typing import Any, Optional

from pydantic import BaseModel, Field

from app.schemas.auth import UserMeResponse
from app.schemas.dashboard import DashboardSummaryResponse
from app.schemas.event import EventEngineResponse


class ComplianceBootstrapSummary(BaseModel):
    kpis: dict[str, Any]
    topViolations: dict[str, Any]


class WorkflowBootstrapSummary(BaseModel):
    compliance: dict[str, Any]
    dashboard: dict[str, Any]
    recentCrossings: dict[str, Any]


class CameraBootstrapSummary(BaseModel):
    health: dict[str, Any]
    cameras: list[dict[str, Any]]


class RecentEventsBootstrap(BaseModel):
    items: list[EventEngineResponse]
    total: int
    page: int
    limit: int


class NotificationBootstrapSummary(BaseModel):
    totalRules: int
    enabledRules: int
    gmail: dict[str, Any] = Field(default_factory=dict)


class DashboardBootstrapResponse(BaseModel):
    user: UserMeResponse
    dashboardSummary: DashboardSummaryResponse
    complianceSummary: ComplianceBootstrapSummary
    workflowSummary: WorkflowBootstrapSummary
    cameraSummary: CameraBootstrapSummary
    recentEvents: RecentEventsBootstrap
    notificationSummary: NotificationBootstrapSummary
    systemHealth: dict[str, Any] = Field(default_factory=dict)
