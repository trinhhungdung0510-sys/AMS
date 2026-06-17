from pydantic import BaseModel, ConfigDict


class LicenseResponse(BaseModel):
    id: str
    farm_id: str
    plan: str
    max_cameras: int
    max_ai_models: int
    start_date: str
    end_date: str
    status: str

    model_config = ConfigDict(from_attributes=True)
