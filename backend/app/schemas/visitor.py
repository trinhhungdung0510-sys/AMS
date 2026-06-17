from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VisitorBase(BaseModel):
    visitor_name: str = Field(min_length=2, max_length=120)
    company: str = Field(min_length=1, max_length=120)
    vehicle_plate: str = Field(default="", max_length=20)
    visit_purpose: str = Field(min_length=2, max_length=255)
    arrival_time: Optional[str] = None
    departure_time: Optional[str] = None
    approved_by: str = Field(min_length=2, max_length=120)


class VisitorCreate(VisitorBase):
    id: Optional[str] = None


class VisitorUpdate(BaseModel):
    visitor_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    company: Optional[str] = Field(default=None, min_length=1, max_length=120)
    vehicle_plate: Optional[str] = Field(default=None, max_length=20)
    visit_purpose: Optional[str] = Field(default=None, min_length=2, max_length=255)
    arrival_time: Optional[str] = None
    departure_time: Optional[str] = None
    approved_by: Optional[str] = Field(default=None, min_length=2, max_length=120)


class VisitorCheckInRequest(BaseModel):
    arrival_time: Optional[str] = None


class VisitorCheckOutRequest(BaseModel):
    departure_time: Optional[str] = None


class VisitorResponse(VisitorBase):
    id: str
    status: str

    model_config = ConfigDict(from_attributes=True)
