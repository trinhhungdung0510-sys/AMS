from __future__ import annotations

import json

from pydantic import BaseModel, ConfigDict, Field


class FarmMapLayerInput(BaseModel):
    layer_key: str
    visible: bool = True
    opacity: float = 1.0


class FarmRouteInput(BaseModel):
    id: str
    route_type: str
    name: str
    points: list[list[float]] = Field(default_factory=list)
    labels: list[str] = Field(default_factory=list)
    valid: bool = True


class FarmObjectInput(BaseModel):
    id: str
    object_type: str
    name: str
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


class FarmLayoutInput(BaseModel):
    farm_id: str = "FARM-001"
    name: str = "Sơ đồ trang trại"
    address: str = ""
    center_lat: float
    center_lng: float
    zoom: int = 17
    base_layer: str = "satellite"
    is_template: bool = False


class SmartFarmSaveRequest(BaseModel):
    layout: FarmLayoutInput
    objects: list[FarmObjectInput] = Field(default_factory=list)
    routes: list[FarmRouteInput] = Field(default_factory=list)
    layers: list[FarmMapLayerInput] = Field(default_factory=list)


class FarmLayoutResponse(BaseModel):
    id: str
    farm_id: str
    name: str
    address: str
    center_lat: float
    center_lng: float
    zoom: int
    base_layer: str
    is_template: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class FarmObjectResponse(FarmObjectInput):
    layout_id: str | None = None

    model_config = ConfigDict(from_attributes=True)


class FarmRouteResponse(BaseModel):
    id: str
    layout_id: str
    route_type: str
    name: str
    points: list[list[float]]
    labels: list[str]
    valid: bool

    model_config = ConfigDict(from_attributes=True)


class FarmMapLayerResponse(BaseModel):
    id: str
    layout_id: str
    layer_key: str
    visible: bool
    opacity: float

    model_config = ConfigDict(from_attributes=True)


class SmartFarmFullResponse(BaseModel):
    layout: FarmLayoutResponse
    objects: list[FarmObjectResponse]
    routes: list[FarmRouteResponse]
    layers: list[FarmMapLayerResponse]


def parse_route_points(raw: str) -> list[list[float]]:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return []


def parse_route_labels(raw: str) -> list[str]:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return []
