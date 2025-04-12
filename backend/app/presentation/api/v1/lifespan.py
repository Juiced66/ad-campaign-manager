from datetime import date, timedelta
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from faker import Faker
from app.application.schemas.campaign import CampaignCreate
from app.application.use_cases.campaign.services import create_campaign
from app.domain.interfaces.campaign_repository import ICampaignRepository
from app.infrastructure.database.sql_alchemy.init_db import init_db
from app.infrastructure.database.sql_alchemy.models.base import Base
from app.infrastructure.database.sql_alchemy.models.campaign import Campaign  # noqa: F401
from app.infrastructure.database.sql_alchemy.models.user import User  # noqa: F401
from app.infrastructure.database.sql_alchemy.models.token import RefreshTokenModel   # noqa: F401
from app.infrastructure.database.sql_alchemy.session import SessionLocal, engine
from app.presentation.api.v1.dependencies.repositories import get_campaign_repository
from app.application.schemas.campaign import CampaignCreate

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created or already exist.")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise
    try:
        with SessionLocal() as db:
            init_db(db)
        logger.info("Database initialization complete.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

    repo = get_campaign_repository(SessionLocal())

    if repo.count_filtered() == 0:
        create_campaign_fixtures(repo)
        logger.info("Campaign fixtures created.")

    yield

    logger.info("Application shutting down...")


def create_campaign_fixtures(repo: ICampaignRepository, count: int = 50):
    fake = Faker()
    today = date.today()
    
    for i in range(count):
        start_offset = fake.random_int(min=0, max=30)
        end_offset = fake.random_int(min=1, max=60)
        start_date = today - timedelta(days=start_offset)
        end_date = start_date + timedelta(days=end_offset)

        dto = CampaignCreate(
            name=fake.company(),
            description=fake.catch_phrase(),
            start_date=start_date,
            end_date=end_date,
            is_active=fake.boolean(chance_of_getting_true=70),
            budget=round(fake.pyfloat(left_digits=5, right_digits=2, positive=True), 2)
        )

        create_campaign(repo, dto)