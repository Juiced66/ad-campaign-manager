import time
from datetime import datetime, timedelta, timezone
from typing import Callable

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.application.schemas.token import Token as TokenResponseSchema

from app.core.security import create_refresh_token_string
from app.infrastructure.database.sql_alchemy.models.token import RefreshTokenModel

@pytest.fixture(scope="function")
def create_test_refresh_token(db_session: Session) -> Callable[..., RefreshTokenModel]:
    def _create(user_id: int, expires_in_days: int = 7, revoked_at: datetime | None = None) -> RefreshTokenModel:
        token_value = create_refresh_token_string()
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
        expires_at_naive = expires_at.replace(tzinfo=None)
        revoked_at_naive = revoked_at.replace(tzinfo=None) if revoked_at else None
        created_at_naive = datetime.now(timezone.utc).replace(tzinfo=None)

        token_model = RefreshTokenModel(
            token_value=token_value,
            user_id=user_id,
            expires_at=expires_at_naive,
            created_at=created_at_naive,
            revoked_at=revoked_at_naive,
        )
        db_session.add(token_model)
        db_session.flush()
        db_session.commit()
        db_session.refresh(token_model)
        return token_model
    return _create

def test_login_success(client: TestClient, create_test_user):
    email = "testlogin@example.com"
    password = "goodpassword"
    create_test_user(email=email, password=password, is_active=True)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    try:
        TokenResponseSchema(**data)
    except Exception as e:
        pytest.fail(f"Login response does not match Token schema: {e}")

    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert "refresh_token" in data
    assert isinstance(data["refresh_token"], str)
    assert data["token_type"] == "bearer"


def test_login_incorrect_password(client: TestClient, create_test_user):
    email = "wrongpass@example.com"
    password = "goodpassword"
    create_test_user(email=email, password=password, is_active=True)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_user_not_found(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nosuchuser@example.com", "password": "anypassword"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_inactive_user(client: TestClient, create_test_user):
    email = "inactive@example.com"
    password = "password"
    create_test_user(email=email, password=password, is_active=False) # Create inactive user

    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 403 # Inactive user should get 403
    assert "Inactive user" in response.json()["detail"]


def test_login_invalid_payload(client: TestClient):
    response = client.post("/api/v1/auth/login", json={"email": "test@example.com"})
    assert response.status_code == 422

    response = client.post("/api/v1/auth/login", json={"password": "password"})
    assert response.status_code == 422

    response = client.post(
        "/api/v1/auth/login", json={"email": "not-an-email", "password": "password"}
    )
    assert response.status_code == 422


def test_refresh_token_success(client: TestClient, create_test_user, create_test_refresh_token, db_session: Session):
    user = create_test_user(email="refresh@test.com", password="password", is_active=True)
    refresh_token_model = create_test_refresh_token(user_id=user.id)

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token_model.token_value}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["refresh_token"] != refresh_token_model.token_value

    db_session.refresh(refresh_token_model)
    assert refresh_token_model.revoked_at is not None

def test_refresh_token_invalid(client: TestClient):
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "invalid-or-nonexistent-token"}
    )
    assert response.status_code == 401
    assert "Invalid refresh token" in response.json()["detail"]

def test_refresh_token_expired(client: TestClient, create_test_user, create_test_refresh_token):
    user = create_test_user(email="refresh_expired@test.com", password="password", is_active=True)
    refresh_token_model = create_test_refresh_token(user_id=user.id, expires_in_days=-1)

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token_model.token_value}
    )
    assert response.status_code == 401
    assert "Refresh token has expired" in response.json()["detail"]

def test_refresh_token_revoked(client: TestClient, create_test_user, create_test_refresh_token):
    user = create_test_user(email="refresh_revoked@test.com", password="password", is_active=True)
    refresh_token_model = create_test_refresh_token(user_id=user.id, revoked_at=datetime.now(timezone.utc))

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token_model.token_value}
    )
    assert response.status_code == 401
    assert "Refresh token has been revoked" in response.json()["detail"]

def test_refresh_token_user_inactive(client: TestClient, create_test_user, create_test_refresh_token, db_session: Session):
    user = create_test_user(email="refresh_inactive@test.com", password="password", is_active=False) # User inactive
    refresh_token_model = create_test_refresh_token(user_id=user.id)

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token_model.token_value}
    )
    assert response.status_code == 401
    assert "User not found or inactive" in response.json()["detail"]

    # The service should revoke the token if the user is inactive
    db_session.refresh(refresh_token_model)
    assert refresh_token_model.revoked_at is not None

def test_logout_success(client: TestClient, create_test_user, create_test_refresh_token, db_session: Session):
    user = create_test_user(email="logout@test.com", password="password", is_active=True)
    refresh_token_model = create_test_refresh_token(user_id=user.id)

    response = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refresh_token_model.token_value}
    )

    assert response.status_code == 204

    db_session.refresh(refresh_token_model)
    assert refresh_token_model.revoked_at is not None

def test_logout_invalid_token(client: TestClient):
    response = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": "non-existent-token"}
    )
    assert response.status_code == 204

def test_logout_already_revoked_token(client: TestClient, create_test_user, create_test_refresh_token, db_session: Session):
    user = create_test_user(email="logout_revoked@test.com", password="password", is_active=True)
    revoked_time = datetime.now(timezone.utc)
    refresh_token_model = create_test_refresh_token(user_id=user.id, revoked_at=revoked_time)

    response = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refresh_token_model.token_value}
    )

    assert response.status_code == 204
    db_session.refresh(refresh_token_model)
    assert refresh_token_model.revoked_at is not None
    # Ensure the timestamp wasn't updated unnecessarily (might be slightly different due to precision)
    assert abs((refresh_token_model.revoked_at.replace(tzinfo=None) - revoked_time.replace(tzinfo=None)).total_seconds()) < 1