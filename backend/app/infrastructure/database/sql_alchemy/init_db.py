import logging

from sqlalchemy.orm import Session

from app.application.schemas.user import UserCreate
from app.application.use_cases.user import services as user_service
from app.core.config import settings
from app.infrastructure.repositories.sql_alchemy.user import SQLAlchemyUserRepository

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """
    Initializes the database with essential data.
    Currently focuses on creating the first superuser if configured.
    NOTE: This runs within the lifespan startup event.
    """

    if not settings.FIRST_SUPERUSER_EMAIL or not settings.FIRST_SUPERUSER_PASSWORD:
        logger.info(
            "Skipping superuser creation: FIRST_SUPERUSER_EMAIL or FIRST_SUPERUSER_PASSWORD missing .env"
        )
        return
    repo = SQLAlchemyUserRepository(db)
    user = user_service.get_user_by_email(repo, email=settings.FIRST_SUPERUSER_EMAIL)

    if not user:
        logger.info("Creating superuser: %s", settings.FIRST_SUPERUSER_EMAIL)        
        try:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
            )

            user_service.create_user(repo=repo, dto=user_in, is_superuser=True)

            logger.info("Superuser created successfully.")
        except Exception as e:
            logger.error(
                "Failed to create superuser %s: %s",
                settings.FIRST_SUPERUSER_EMAIL,
                e,
                exc_info=True
            )
            db.rollback()
    else:
        logger.info(
            "Superuser %s already exists. Skipping creation.",
            settings.FIRST_SUPERUSER_EMAIL,
        )
