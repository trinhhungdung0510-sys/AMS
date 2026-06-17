from pydantic import BaseModel, ConfigDict


class FarmMapObjectResponse(BaseModel):
    id: str
    object_type: str
    name: str
    zone: str
    x: float
    y: float
    status: str

    model_config = ConfigDict(from_attributes=True)
