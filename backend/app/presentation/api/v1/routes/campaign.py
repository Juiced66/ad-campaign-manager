from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.application.schemas.campaign import Campaign, CampaignCreate, CampaignUpdate
from app.application.use_cases.campaign import services as campaign_services
from app.domain.entities.user import User as DomainUser
from app.domain.interfaces.campaign_repository import ICampaignRepository
from app.presentation.api.v1.dependencies.auth import get_current_user
from app.presentation.api.v1.dependencies.repositories import get_campaign_repository

router = APIRouter()


@router.get("/", response_model=List[Campaign])
def list_campaigns(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    repo: ICampaignRepository = Depends(get_campaign_repository),
    _: DomainUser = Depends(get_current_user),
):
    return campaign_services.get_campaigns(
        repo,
        skip=skip,
        limit=limit,
        is_active=is_active,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/{campaign_id}", response_model=Campaign)
def get_campaign(
    campaign_id: int,
    repo: ICampaignRepository = Depends(get_campaign_repository),
    _: DomainUser = Depends(get_current_user),
):
    campaign = campaign_services.get_campaign(repo, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.post("/", response_model=Campaign, status_code=201)
def create_campaign(
    campaign_in: CampaignCreate,
    repo: ICampaignRepository = Depends(get_campaign_repository),
    _: DomainUser = Depends(get_current_user),
):
    return campaign_services.create_campaign(repo, campaign_in)


@router.put("/{campaign_id}", response_model=Campaign)
def update_campaign(
    campaign_id: int,
    campaign_in: CampaignUpdate,
    repo: ICampaignRepository = Depends(get_campaign_repository),
    _: DomainUser = Depends(get_current_user),
):
    updated = campaign_services.update_campaign(repo, campaign_id, campaign_in)
    if updated is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return updated


@router.delete("/{campaign_id}", response_model=Campaign)
def delete_campaign(
    campaign_id: int,
    repo: ICampaignRepository = Depends(get_campaign_repository),
    _: DomainUser = Depends(get_current_user),
):
    deleted = campaign_services.delete_campaign(repo, campaign_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return deleted
