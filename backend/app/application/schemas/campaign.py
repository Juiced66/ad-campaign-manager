from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class CampaignBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    start_date: date
    end_date: date
    budget: float = Field(..., gt=0)
    is_active: bool = Field(default=False)


@field_validator("end_date")
@classmethod
def end_date_must_be_after_start_date(cls, end_date: date, info: ValidationInfo):
    start_date = info.data.get("start_date")
    if start_date and end_date < start_date:
        raise ValueError("End date must be after start date")
    return end_date


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None


@field_validator("end_date")
@classmethod
def end_date_must_be_after_start_date(cls, end_date: date, info: ValidationInfo):
    start_date = info.data.get("start_date")
    if start_date and end_date < start_date:
        raise ValueError("End date must be after start date")
    return end_date


class Campaign(CampaignBase):
    id: int

    model_config = {"from_attributes": True}
