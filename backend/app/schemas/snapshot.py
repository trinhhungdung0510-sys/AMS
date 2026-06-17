from pydantic import BaseModel, ConfigDict


class EventSnapshotResponse(BaseModel):
    id: str
    event_id: str
    image_path: str
    thumbnail_path: str

    model_config = ConfigDict(from_attributes=True)
