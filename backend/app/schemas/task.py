from typing import Optional

from pydantic import BaseModel, ConfigDict


class AITaskResponse(BaseModel):
    id: str
    camera_id: str
    category: str
    status: str
    priority: int
    result: str
    created_at: str
    processed_at: Optional[str]

    model_config = ConfigDict(from_attributes=True)
