from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    tong_camera: int
    tong_trang_trai: int
    tong_canh_bao_ai: int
    camera_truc_tuyen: int
    tong_su_kien: int
    su_kien_rui_ro_cao: int
    su_kien_dang_mo: int


class DashboardTrendItem(BaseModel):
    ngay: str
    su_kien: int


class DashboardTopCameraItem(BaseModel):
    camera_id: str
    ten_camera: str
    ten_vung: str
    so_su_kien: int


class DashboardTopZoneItem(BaseModel):
    ten_vung: str
    so_su_kien: int
    nghiem_trong: int
