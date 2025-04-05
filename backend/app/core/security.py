import logging
from datetime import datetime, timedelta, timezone
import secrets

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings

logger = logging.getLogger(__name__)


class TokenError(Exception):
    """Custom exception for token related errors."""


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt."""
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token with an expiration.

    Args:
        data: The payload data (e.g., {"sub": user.email}).
        expires_delta: Optional timedelta for token expiration.

    Returns:
        A JWT token string.

    Raises:
        TokenError: If token encoding fails.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})

    try:
        token = jwt.encode(
            to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM
        )
        return token
    except Exception as e:
        logger.error("Error encoding token: %s", e, exc_info=True)
        raise TokenError("Could not create access token") from e

def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.

    Args:
        token: The JWT token string.

    Returns:
        The decoded payload as a dictionary.

    Raises:
        TokenError: If token decoding or validation fails.
    """
    try:
        payload = jwt.decode(
            token, settings.AUTH_SECRET_KEY, algorithms=[settings.AUTH_ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.error("Token decode error: %s", e, exc_info=True)
        raise TokenError("Invalid token") from e

def create_refresh_token_string() -> str:
    """Generates a cryptographically secure random string for refresh tokens."""
    return secrets.token_urlsafe(32)
