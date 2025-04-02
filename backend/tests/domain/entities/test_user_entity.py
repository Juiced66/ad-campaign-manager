from app.domain.entities.user import User


def test_user_creation():
    user = User(
        email="test@example.com",
        hashed_password="hashed",
        is_active=True,
        is_superuser=False,
    )
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.is_superuser is False


def test_user_activate_deactivate():
    user = User(email="test@example.com", hashed_password="hashed", is_active=False)
    assert user.is_active is False
    user.activate()
    assert user.is_active is True
    user.deactivate()
    assert user.is_active is False
