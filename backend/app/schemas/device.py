from pydantic import BaseModel, ConfigDict


class EdgeDeviceResponse(BaseModel):
    id: str
    farm_id: str
    device_name: str
    device_type: str
    serial_number: str
    status: str
    assigned_cameras: int

    model_config = ConfigDict(from_attributes=True)
