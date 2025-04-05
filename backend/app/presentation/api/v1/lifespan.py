import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database.sql_alchemy.init_db import init_db
from app.infrastructure.database.sql_alchemy.models.base import Base
from app.infrastructure.database.sql_alchemy.models.campaign import Campaign  # noqa: F401
from app.infrastructure.database.sql_alchemy.models.user import User  # noqa: F401
from app.infrastructure.database.sql_alchemy.models.token import RefreshTokenModel   # noqa: F401
from app.infrastructure.database.sql_alchemy.session import SessionLocal, engine

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

    yield

    logger.info("Application shutting down...")
