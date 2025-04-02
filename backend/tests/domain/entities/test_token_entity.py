from datetime import datetime, timedelta, timezone

from app.domain.entities.auth import AccessTokenData


def test_create_token_entity_with_created_at():
    """Test creating a Token entity when created_at is provided."""
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=30)
    token_value = "test.token.value"
    user_id = 1

    token = AccessTokenData(
        access_token=token_value, user_id=user_id, expires_at=expires, created_at=now
    )

    assert token.access_token == token_value
    assert token.user_id == user_id
    assert token.expires_at == expires
    assert token.created_at == now


def test_create_token_entity_without_created_at():
    """Test creating a Token entity when created_at is omitted (should default)."""
    before_creation = datetime.now(timezone.utc)
    expires = before_creation + timedelta(minutes=30)
    token_value = "test.token.value.2"
    user_id = 2

    token = AccessTokenData(
        access_token=token_value,
        user_id=user_id,
        expires_at=expires,
        # created_at is omitted
    )

    after_creation = datetime.now(timezone.utc)

    assert token.access_token == token_value
    assert token.user_id == user_id
    assert token.expires_at == expires
    assert token.created_at is not None
    assert before_creation <= token.created_at <= after_creation
