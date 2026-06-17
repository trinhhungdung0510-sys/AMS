from typing import Optional

from pydantic import BaseModel


class PersonTrackVisitResponse(BaseModel):
    id: str
    zone_id: str
    ten_vung: str
    enter_time: str
    exit_time: Optional[str] = None


class TrackDetailResponse(BaseModel):
    track_id: int
    camera_id: Optional[str] = None
    lich_su_vung: list[PersonTrackVisitResponse] = []
