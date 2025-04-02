from fastapi import Depends
from sqlalchemy.orm import Session

from app.domain.interfaces.campaign_repository import ICampaignRepository
from app.domain.interfaces.token_repository import ITokenRepository
from app.domain.interfaces.user_repository import IUserRepository
from app.infrastructure.database.sql_alchemy.session import get_db
from app.infrastructure.repositories.sql_alchemy.campaign import (
    CampaignSqlAlchemyRepository,
)
from app.infrastructure.repositories.sql_alchemy.token import SQLAlchemyTokenRepository
from app.infrastructure.repositories.sql_alchemy.user import SQLAlchemyUserRepository


def get_campaign_repository(db: Session = Depends(get_db)) -> ICampaignRepository:
    return CampaignSqlAlchemyRepository(db)


def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
    return SQLAlchemyUserRepository(db)


def get_token_repository(db: Session = Depends(get_db)) -> ITokenRepository:
    return SQLAlchemyTokenRepository(db)
