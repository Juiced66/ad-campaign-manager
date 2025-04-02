from unittest.mock import MagicMock, patch

import pytest

from app.application.schemas.user import UserCreate

# You might not need the User domain entity directly in the mocks anymore,
# unless get_user_by_email is expected to return one. Let's assume it does for now.
from app.domain.entities.user import User

# Adjust imports based on your actual project structure
from app.infrastructure.database.sql_alchemy.init_db import init_db


@pytest.fixture
def mock_db_session():
    """Fixture for a mocked synchronous database session."""
    session = MagicMock()
    session.rollback = MagicMock()
    return session


@pytest.fixture
def mock_user_repo():
    """Fixture for a mocked UserRepository instance."""
    # This mock will replace the result of SQLAlchemyUserRepository(db)
    return MagicMock()


# --- Test Cases ---


def test_init_db_skip_creation_if_no_email(mocker, mock_db_session):
    """Test init_db skips creation if FIRST_SUPERUSER_EMAIL is not set."""
    mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.settings.FIRST_SUPERUSER_EMAIL",
        None,
    )
    mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.settings.FIRST_SUPERUSER_PASSWORD",
        "password",
    )

    mock_get_user = mocker.patch(
        "app.application.use_cases.user.services.get_user_by_email"
    )
    mock_create_user = mocker.patch(
        "app.application.use_cases.user.services.create_user"
    )
    mock_repo_class = mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.SQLAlchemyUserRepository"
    )

    init_db(mock_db_session)

    mock_repo_class.assert_not_called()
    mock_get_user.assert_not_called()
    mock_create_user.assert_not_called()


def test_init_db_skip_creation_if_no_password(mocker, mock_db_session):
    """Test init_db skips creation if FIRST_SUPERUSER_PASSWORD is not set."""
    mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.settings.FIRST_SUPERUSER_EMAIL",
        "admin@test.com",
    )
    mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.settings.FIRST_SUPERUSER_PASSWORD",
        None,
    )

    mock_get_user = mocker.patch(
        "app.application.use_cases.user.services.get_user_by_email"
    )
    mock_create_user = mocker.patch(
        "app.application.use_cases.user.services.create_user"
    )
    mock_repo_class = mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.SQLAlchemyUserRepository"
    )

    init_db(mock_db_session)

    mock_repo_class.assert_not_called()
    mock_get_user.assert_not_called()
    mock_create_user.assert_not_called()


def test_init_db_superuser_already_exists(mocker, mock_db_session, mock_user_repo):
    """Test init_db skips creation if the superuser already exists."""
    test_email = "admin@test.com"
    mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.settings.FIRST_SUPERUSER_EMAIL",
        test_email,
    )
    mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.settings.FIRST_SUPERUSER_PASSWORD",
        "superadmin",
    )

    mock_repo_class = mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.SQLAlchemyUserRepository"
    )
    mock_repo_class.return_value = mock_user_repo

    existing_user = User(email=test_email, hashed_password="abc", is_superuser=True)
    mock_get_user = mocker.patch(
        "app.application.use_cases.user.services.get_user_by_email"
    )
    mock_get_user.return_value = existing_user

    mock_create_user = mocker.patch(
        "app.application.use_cases.user.services.create_user"
    )

    init_db(mock_db_session)

    mock_repo_class.assert_called_once_with(mock_db_session)
    mock_get_user.assert_called_once_with(mock_user_repo, email=test_email)
    mock_create_user.assert_not_called()


def test_init_db_creates_superuser_if_not_exists(
    mocker, mock_db_session, mock_user_repo
):
    """Test init_db creates the superuser if it does not exist."""
    test_email = "admin@test.com"
    test_password = "superadmin"
    mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.settings.FIRST_SUPERUSER_EMAIL",
        test_email,
    )
    mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.settings.FIRST_SUPERUSER_PASSWORD",
        test_password,
    )

    mock_repo_class = mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.SQLAlchemyUserRepository"
    )
    mock_repo_class.return_value = mock_user_repo

    mock_get_user = mocker.patch(
        "app.application.use_cases.user.services.get_user_by_email"
    )
    mock_get_user.return_value = None

    mock_create_user = mocker.patch(
        "app.application.use_cases.user.services.create_user"
    )

    init_db(mock_db_session)

    mock_repo_class.assert_called_once_with(mock_db_session)
    mock_get_user.assert_called_once_with(mock_user_repo, email=test_email)

    mock_create_user.assert_called_once()

    call_args, call_kwargs = mock_create_user.call_args
    assert call_kwargs.get("repo") == mock_user_repo
    assert call_kwargs.get("is_superuser") is True
    dto_arg = call_kwargs.get("dto")
    assert isinstance(dto_arg, UserCreate)
    assert dto_arg.email == test_email
    assert dto_arg.password == test_password


def test_init_db_handles_creation_exception(mocker, mock_db_session, mock_user_repo):
    """Test init_db handles exceptions during superuser creation and rolls back."""
    test_email = "admin@error.com"
    test_password = "superadmin"
    mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.settings.FIRST_SUPERUSER_EMAIL",
        test_email,
    )
    mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.settings.FIRST_SUPERUSER_PASSWORD",
        test_password,
    )

    mock_repo_class = mocker.patch(
        "app.infrastructure.database.sql_alchemy.init_db.SQLAlchemyUserRepository"
    )
    mock_repo_class.return_value = mock_user_repo

    mock_get_user = mocker.patch(
        "app.application.use_cases.user.services.get_user_by_email"
    )
    mock_get_user.return_value = None

    mock_create_user = mocker.patch(
        "app.application.use_cases.user.services.create_user"
    )
    creation_error = ValueError("DB constraint failed")
    mock_create_user.side_effect = creation_error

    with patch("builtins.print") as mock_print:
        init_db(mock_db_session)

    mock_repo_class.assert_called_once_with(mock_db_session)
    mock_get_user.assert_called_once_with(mock_user_repo, email=test_email)
    mock_create_user.assert_called_once()

    mock_db_session.rollback.assert_called_once()
