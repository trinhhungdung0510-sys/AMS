from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FarmMapLayoutResponse(BaseModel):
    id: str
    farm_id: str
    name: str
    is_template: bool
    is_active: bool
    center_lat: float
    center_lng: float
    zoom: int
    base_layer: str

    model_config = ConfigDict(from_attributes=True)


class FarmMapLayoutSaveRequest(BaseModel):
    farm_id: str = "FARM-001"
    name: str = "Bản đồ trang trại"
    is_template: bool = False
    center_lat: float
    center_lng: float
    zoom: int = 17
    base_layer: str = "satellite"


class FarmMapObjectResponse(BaseModel):
    id: str
    layout_id: str | None = None
    object_type: str
    name: str
    zone: str = ""
    description: str = ""
    x: float
    y: float
    width: float
    height: float
    rotation: float
    atsh_zone_type: str = "buffer"
    atsh_level: str = "green"
    linked_camera_id: str | None = None
    linked_zone_id: str | None = None
    camera_direction: float | None = None
    camera_fov: float | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class FarmMapObjectInput(BaseModel):
    id: str
    object_type: str
    name: str
    zone: str = ""
    description: str = ""
    x: float
    y: float
    width: float = 0.0003
    height: float = 0.0003
    rotation: float = 0
    atsh_zone_type: str = "buffer"
    atsh_level: str = "green"
    linked_camera_id: str | None = None
    linked_zone_id: str | None = None
    camera_direction: float | None = None
    camera_fov: float | None = None
    status: str = "active"


class FarmMapSaveRequest(BaseModel):
    layout: FarmMapLayoutSaveRequest
    objects: list[FarmMapObjectInput] = Field(default_factory=list)


class FarmMapFullResponse(BaseModel):
    layout: FarmMapLayoutResponse
    objects: list[FarmMapObjectResponse]
