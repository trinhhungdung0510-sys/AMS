from typing import Optional

from pydantic import BaseModel


class CameraSnapshotResponse(BaseModel):
    success: bool
    url: Optional[str] = None
    error: Optional[str] = None
    captured_at: Optional[str] = None
