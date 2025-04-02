from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import (
    TokenError,
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing_and_verification():
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)

    assert isinstance(hashed_password, str)
    assert len(hashed_password) > len(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False


def test_create_and_decode_valid_token():
    data = {"sub": "test@example.com", "custom_data": 123}
    token = create_access_token(data)
    assert isinstance(token, str)

    payload = decode_access_token(token)
    assert payload["sub"] == data["sub"]
    assert payload["custom_data"] == data["custom_data"]
    assert "exp" in payload


def test_decode_invalid_token_signature():
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {"sub": "test@example.com", "exp": expire}

    invalid_token = jwt.encode(
        payload, "wrongsecret", algorithm=settings.AUTH_ALGORITHM
    )

    with pytest.raises(
        TokenError, match="Invalid token"
    ):
        decode_access_token(invalid_token)


def test_decode_expired_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data, expires_delta=timedelta(minutes=-1))

    with pytest.raises(
        TokenError, match="Invalid token"
    ):
        decode_access_token(token)
