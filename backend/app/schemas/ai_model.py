from pydantic import BaseModel, ConfigDict


class AIModelResponse(BaseModel):
    id: str
    model_name: str
    model_type: str
    version: str
    enabled: bool

    model_config = ConfigDict(from_attributes=True)
