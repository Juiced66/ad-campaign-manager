from abc import abstractmethod
from datetime import date
from typing import List, Optional

from app.domain.entities.campaign import Campaign
from app.domain.interfaces.base_repository import IRepository


class ICampaignRepository(IRepository[Campaign]):
    @abstractmethod
    def get_multi_filtered(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Campaign]: ...
