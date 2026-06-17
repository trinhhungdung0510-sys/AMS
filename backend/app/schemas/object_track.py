from typing import Optional

from pydantic import BaseModel, ConfigDict


class ObjectTrackSyncItem(BaseModel):
    track_id: int
    camera_id: str
    object_type: str
    current_zone: str
    previous_zone: Optional[str] = None
    enter_time: str
    leave_time: Optional[str] = None
    last_seen: str
    confidence: float = 0.0
    employee_id: Optional[str] = None


class ObjectTrackSyncRequest(BaseModel):
    tracks: list[ObjectTrackSyncItem]


class ObjectTrackIdentifyRequest(BaseModel):
    employee_id: str
    camera_id: str


class ObjectTrackResponse(BaseModel):
    id: str
    track_id: int
    camera_id: str
    object_type: str
    current_zone: str
    previous_zone: Optional[str]
    employee_id: Optional[str]
    employee_code: Optional[str] = None
    employee_name: Optional[str] = None
    assigned_zone: Optional[str] = None
    zone_match: Optional[bool] = None
    enter_time: str
    leave_time: Optional[str]
    last_seen: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)
