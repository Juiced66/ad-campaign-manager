from datetime import date
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.domain.entities.campaign import Campaign
from app.domain.interfaces.campaign_repository import ICampaignRepository
from app.infrastructure.database.sql_alchemy.models.campaign import (
    Campaign as CampaignModel,
)
from app.infrastructure.repositories.sql_alchemy.base import SQLAlchemyBaseRepository


class CampaignSqlAlchemyRepository(
    SQLAlchemyBaseRepository[CampaignModel, Campaign], ICampaignRepository
):
    def __init__(self, db: Session):
        super().__init__(db, CampaignModel, Campaign)

    def get_multi_filtered(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Campaign]:
        filters = []
        if is_active is not None:
            filters.append(self.model.is_active == is_active)
        if start_date is not None:
            filters.append(self.model.start_date >= start_date)
        if end_date is not None:
            filters.append(self.model.end_date <= end_date)

        query = self.db.query(self.model)
        if filters:
            query = query.filter(and_(*filters))

        results = query.offset(skip).limit(limit).all()
        return [self._to_entity(obj) for obj in results if obj is not None]

    def _create_entity_instance(self, db_obj: CampaignModel) -> Campaign:
        return Campaign(
            name=db_obj.name,
            description=db_obj.description,
            start_date=db_obj.start_date,
            end_date=db_obj.end_date,
            budget=db_obj.budget,
            is_active=db_obj.is_active,
        )

    def _from_entity(self, entity: Campaign) -> CampaignModel:
        return CampaignModel(
            id=getattr(entity, "id", None),
            name=entity.name,
            description=entity.description,
            start_date=entity.start_date,
            end_date=entity.end_date,
            budget=entity.budget,
            is_active=entity.is_active,
        )
