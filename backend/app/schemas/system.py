from typing import Any

from pydantic import BaseModel, Field


class SystemSettingsResponse(BaseModel):
    compliance_threshold: float = Field(ge=0, le=1)
    workflow_timeout: int = Field(ge=30, le=86400)
    demo_mode: bool
    retention_days: int = Field(ge=1, le=3650)


class SystemSettingsUpdate(BaseModel):
    compliance_threshold: float | None = Field(default=None, ge=0, le=1)
    workflow_timeout: int | None = Field(default=None, ge=30, le=86400)
    demo_mode: bool | None = None
    retention_days: int | None = Field(default=None, ge=1, le=3650)


class BackupRestoreResponse(BaseModel):
    version: str
    exportedAt: str
    settings: dict[str, Any]
    farms: list[dict[str, Any]]
    cameras: list[dict[str, Any]]
    zones: list[dict[str, Any]]
    workflows: list[dict[str, Any]]
    uniforms: list[dict[str, Any]]


class RestoreRequest(BaseModel):
    version: str | None = None
    settings: dict[str, Any] | None = None
    farms: list[dict[str, Any]] | None = None
    cameras: list[dict[str, Any]] | None = None
    zones: list[dict[str, Any]] | None = None
    workflows: list[dict[str, Any]] | None = None
    uniforms: list[dict[str, Any]] | None = None
