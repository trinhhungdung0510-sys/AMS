from typing import Any, Optional

from pydantic import BaseModel, Field


class DeploymentHealthResponse(BaseModel):
    status: str
    service: str
    version: str = "2.0"
    database: str
    redis: str
    websocket: dict[str, Any]
    storage: dict[str, Any]
    camera: dict[str, Any]
    ffmpeg: dict[str, Any]


class RuleTestRequest(BaseModel):
    ruleType: str = Field(min_length=2)
    trackId: Optional[int] = None
    cameraId: Optional[str] = None
    zoneId: Optional[str] = None
    score: Optional[float] = Field(default=None, ge=0, le=1)


class ConfigImportRequest(BaseModel):
    farm: Optional[list[dict[str, Any]]] = Field(default=None, alias="farm.json")
    camera: Optional[list[dict[str, Any]]] = Field(default=None, alias="camera.json")
    zone: Optional[list[dict[str, Any]]] = Field(default=None, alias="zone.json")
    workflow: Optional[list[dict[str, Any]]] = Field(default=None, alias="workflow.json")
    settings: Optional[dict[str, Any]] = Field(default=None, alias="settings.json")
    uniform: Optional[list[dict[str, Any]]] = Field(default=None, alias="uniform.json")

    model_config = {"populate_by_name": True}
