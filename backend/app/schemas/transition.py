from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ZoneCrossingInput(BaseModel):
    track_id: int
    camera_id: str
    zone_id: str
    timestamp: str
    object_type: Optional[str] = None


class ZoneTransitionCreate(BaseModel):
    object_type: str
    track_id: int
    camera_id: str = "CAM-001"
    from_zone: str
    to_zone: str
    cross_time: str
    timestamp: Optional[str] = None


class ZoneTransitionResponse(BaseModel):
    id: str
    track_id: int
    object_type: str
    camera_id: str
    from_zone: str
    to_zone: str
    cross_time: str

    model_config = ConfigDict(from_attributes=True)


class RecentZoneCrossingsResponse(BaseModel):
    total: int
    items: list[ZoneTransitionResponse]
