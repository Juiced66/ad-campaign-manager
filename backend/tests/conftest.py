# tests/conftest.py

from datetime import date
from typing import Any, Callable, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.security import get_password_hash

from app.infrastructure.database.sql_alchemy.models.base import Base
from app.infrastructure.database.sql_alchemy.models.campaign import (
    Campaign as CampaignModel,
)

from app.infrastructure.database.sql_alchemy.models.user import User as UserModel
from app.infrastructure.database.sql_alchemy.session import get_db
from app.presentation.api.v1.main import lifespan
from app.presentation.api.v1.routes import auth, campaign, user


@pytest.fixture(scope="session")
def test_db_url() -> str:
    return "sqlite:///:memory:"


@pytest.fixture(scope="session")
def test_engine(test_db_url: str):
    engine = create_engine(
        test_db_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="session")
def TestingSessionLocal(test_engine):
    return sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine, expire_on_commit=False
    )


@pytest.fixture(scope="function")
def db_session(test_engine, TestingSessionLocal) -> Generator[Session, None, None]:
    """Provides a transactional database session per test function."""
    connection = test_engine.connect()
    connection.begin()
    db = TestingSessionLocal(bind=connection)
    try:
        yield db
    finally:
        db.rollback()
        connection.close()


@pytest.fixture(scope="function")
def override_get_db(db_session: Session) -> Callable[[], Generator[Session, Any, None]]:
    """
    Dependency override function that yields the *SAME* session
    instance (db_session) provided by the db_session fixture.
    """

    def _override_get_db() -> Generator[Session, Any, None]:
        yield db_session

    return _override_get_db


@pytest.fixture(scope="function")
def test_app(override_get_db: Callable[[], Generator[Session, Any, None]]) -> FastAPI:
    """Creates a new FastAPI app instance for testing with overrides applied."""
    app = FastAPI(lifespan=lifespan)

    api_prefix = settings.API_V1_STR

    app.include_router(user.router, prefix=f"{api_prefix}/users", tags=["Users"])
    app.include_router(
        campaign.router, prefix=f"{api_prefix}/campaigns", tags=["Campaigns"]
    )
    app.include_router(
        auth.router, prefix=f"{api_prefix}/auth", tags=["Authentication"]
    )

    @app.get("/")
    def read_root_test():
        return {"message": "Test App Root"}

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture(scope="function")
def client(test_app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(test_app, base_url="http://testserver") as tc:
        yield tc


@pytest.fixture(scope="function")
def create_test_user(db_session: Session) -> Callable[..., UserModel]:
    """Fixture factory to create User models (uses db_session, flushes)."""

    def _create_test_user_factory(
        email: str, password: str, is_active: bool = True, is_superuser: bool = False
    ) -> UserModel:
        hashed_password = get_password_hash(password)
        user = UserModel(
            email=email,
            hashed_password=hashed_password,
            is_active=is_active,
            is_superuser=is_superuser,
        )
        db_session.add(user)
        db_session.flush()
        return user

    return _create_test_user_factory


@pytest.fixture(scope="function")
def create_test_campaign(db_session: Session) -> Callable[..., CampaignModel]:
    """Fixture factory to create Campaign models (uses db_session, flushes)."""

    def _create_test_campaign_factory(
        name: str,
        start_date: date,
        end_date: date,
        budget: float,
        description: str | None = None,
        is_active: bool = False,
    ) -> CampaignModel:
        if description is None:
            description = f"Test description for {name}"
        campaign = CampaignModel(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            is_active=is_active,
        )
        db_session.add(campaign)
        db_session.flush()
        return campaign

    return _create_test_campaign_factory


@pytest.fixture(scope="function")
def test_auth_headers(client: TestClient, create_test_user) -> dict[str, str]:
    """Fixture to get authentication headers for a default test user."""
    email = "authtest@example.com"
    password = "testpassword"

    create_test_user(email=email, password=password, is_active=True)

    login_response = client.post(
        f"{settings.API_V1_STR}/auth/login", json={"email": email, "password": password}
    )

    login_response.raise_for_status()

    token_data = login_response.json()
    token = token_data["access_token"]
    return {"Authorization": f"Bearer {token}"}
