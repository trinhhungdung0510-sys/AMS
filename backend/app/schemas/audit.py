from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: str
    farm_id: Optional[str] = None
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    metadata_json: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)
