from pydantic import BaseModel, ConfigDict, Field


class EventResponse(BaseModel):
    id: str
    ten_vi_pham: str
    muc_do: str
    ten_vung: str
    ten_camera: str
    ten_trang_trai: str
    do_tin_cay: int
    thoi_gian: str
    trang_thai: str
    nguoi_xu_ly: str

    model_config = ConfigDict(from_attributes=True)


class EmailAlertPreview(BaseModel):
    tieu_de: str
    noi_dung: str
