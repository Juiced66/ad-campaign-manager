from datetime import date
from typing import List, Optional

from app.application.schemas.campaign import Campaign as CampaignSchema
from app.application.schemas.campaign import CampaignCreate, CampaignUpdate
from app.domain.entities.campaign import Campaign
from app.domain.interfaces.campaign_repository import ICampaignRepository
from app.infrastructure.database.sql_alchemy.models import Campaign as CampaignModel


def get_campaigns(
    repo: ICampaignRepository,
    *,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[Campaign]:
    return repo.get_multi_filtered(
        skip=skip,
        limit=limit,
        is_active=is_active,
        start_date=start_date,
        end_date=end_date,
    )


def create_campaign(repo: ICampaignRepository, dto: CampaignCreate) -> Campaign:
    entity = Campaign(**dto.model_dump())
    return repo.create(entity=entity)


def get_campaign(repo: ICampaignRepository, campaign_id: int) -> Optional[Campaign]:
    return repo.get(id=campaign_id)


def update_campaign(
    repo: ICampaignRepository, campaign_id: int, dto: CampaignUpdate
) -> Optional[Campaign]:
    db_obj: Optional[CampaignModel] = repo.get(id=campaign_id)
    if not db_obj:
        return None
    update_data = dto.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    updated_db_obj = repo.update(id=campaign_id, entity=db_obj)

    if updated_db_obj:
        return CampaignSchema.model_validate(updated_db_obj)
    
    return None


def delete_campaign(repo: ICampaignRepository, campaign_id: int) -> Optional[Campaign]:
    return repo.remove(id=campaign_id)
