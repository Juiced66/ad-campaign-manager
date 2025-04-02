from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.application.schemas.user import UserCreate
from app.application.use_cases.user import services as user_services
from app.core.security import get_password_hash
from app.domain.entities.user import User
from app.domain.interfaces.user_repository import IUserRepository


@pytest.fixture
def mock_user_repo():
    """Fixture for a mocked IUserRepository."""
    repo = MagicMock(spec=IUserRepository)
    repo.get_by_email = MagicMock()
    repo.create = MagicMock()
    repo.update = MagicMock()
    repo.get = MagicMock()
    return repo


@pytest.fixture
def test_user_data():
    """Sample valid user data for creation."""
    return UserCreate(email="test@example.com", password="password123")


@pytest.fixture
def existing_user_entity(test_user_data):
    """A sample User domain entity representing an existing user."""

    hashed_password = get_password_hash(test_user_data.password)
    return User(
        email=test_user_data.email,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False,
    )


def test_create_user_success(mock_user_repo, test_user_data):
    """Test successful user creation."""

    mock_user_repo.get_by_email.return_value = None
    created_user_mock = User(
        email=test_user_data.email, hashed_password="hashed_pwd", is_superuser=False
    )
    mock_user_repo.create.return_value = created_user_mock

    created_user = user_services.create_user(
        repo=mock_user_repo, dto=test_user_data, is_superuser=False
    )

    mock_user_repo.create.assert_called_once()

    assert created_user.email == test_user_data.email
    assert created_user.is_superuser is False
    assert created_user.hashed_password != test_user_data.password

    assert created_user == created_user_mock


def test_create_superuser_success(mock_user_repo, test_user_data):
    """Test successful superuser creation."""
    mock_user_repo.get_by_email.return_value = None
    created_user_mock = User(
        email=test_user_data.email, hashed_password="hashed_pwd", is_superuser=True
    )
    mock_user_repo.create.return_value = created_user_mock

    created_user = user_services.create_user(
        repo=mock_user_repo, dto=test_user_data, is_superuser=True
    )

    assert created_user.is_superuser is True
    assert created_user == created_user_mock


def test_create_user_email_exists(mock_user_repo, test_user_data, existing_user_entity):
    """Test user creation failure when email already exists."""
    mock_user_repo.get_by_email.return_value = existing_user_entity

    with pytest.raises(HTTPException) as exc_info:
        user_services.create_user(repo=mock_user_repo, dto=test_user_data)

    assert exc_info.value.status_code == 400
    assert "Email already registered" in exc_info.value.detail
    mock_user_repo.create.assert_not_called()


def test_get_user_by_email_found(mock_user_repo, existing_user_entity):
    """Test retrieving user by email when found."""
    mock_user_repo.get_by_email.return_value = existing_user_entity
    email = existing_user_entity.email

    user = user_services.get_user_by_email(repo=mock_user_repo, email=email)

    mock_user_repo.get_by_email.assert_called_once_with(email=email)
    assert user == existing_user_entity


def test_get_user_by_email_not_found(mock_user_repo):
    """Test retrieving user by email when not found."""
    email = "notfound@example.com"
    mock_user_repo.get_by_email.return_value = None

    user = user_services.get_user_by_email(repo=mock_user_repo, email=email)

    mock_user_repo.get_by_email.assert_called_once_with(email=email)
    assert user is None
