from pydantic import BaseModel, ConfigDict


class FarmResponse(BaseModel):
    id: str
    name: str
    location: str
    plan: str
    status: str

    model_config = ConfigDict(from_attributes=True)
