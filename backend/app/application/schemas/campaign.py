from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class CampaignBase(BaseModel):
    """Base Pydantic schema for campaign data."""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    start_date: date
    end_date: date
    budget: float = Field(..., gt=0)
    is_active: bool = Field(default=False)


@field_validator("end_date")
@classmethod
def end_date_must_be_after_start_date(_, end_date: date, info: ValidationInfo):
    """end date validator"""
    start_date = info.data.get("start_date")
    if start_date and end_date < start_date:
        raise ValueError("End date must be after start date")
    return end_date


class CampaignCreate(CampaignBase):
    """Schema for creating a new campaign."""


class CampaignUpdate(BaseModel):
    """Schema for updating an existing campaign (all fields optional)."""
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None


@field_validator("end_date")
@classmethod
def end_date_must_be_after_start_date_for_update(_, end_date: date, info: ValidationInfo):
    """end date validator"""
    start_date = info.data.get("start_date")
    if start_date and end_date < start_date:
        raise ValueError("End date must be after start date")
    return end_date


class Campaign(CampaignBase):
    """Schema for reading campaign data, including the ID."""
    id: int

    model_config = {"from_attributes": True}
