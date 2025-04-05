import logging
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import (
    TokenError,
    verify_password,
    create_access_token,
    create_refresh_token_string,
)
from app.domain.entities.auth import RefreshToken
from app.domain.entities.user import User as DomainUser
from app.domain.interfaces.token_repository import ITokenRepository
from app.domain.interfaces.user_repository import IUserRepository
from app.application.schemas.token import Token as TokenResponseSchema

logger = logging.getLogger(__name__)

class AuthenticationError(Exception):
    """Custom exception for authentication failures."""
    pass

class AuthorizationError(Exception):
    """Custom exception for authorization failures."""
    pass

class AuthService:
    def __init__(self, user_repo: IUserRepository, token_repo: ITokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    def _create_auth_tokens(self, user: DomainUser) -> TokenResponseSchema:
        """Helper to create access and refresh tokens for a user."""
        # Create Access Token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        try:
            access_token_payload = {"sub": user.email, "user_id": user.id}
            access_token = create_access_token(
                access_token_payload, expires_delta=access_token_expires
            )
        except TokenError as e:
            logger.error(f"Access Token creation failed for user {user.email}: {e}", exc_info=True)
            raise AuthenticationError("Could not create access token") from e

        # Create Refresh Token
        refresh_token_value = create_refresh_token_string()
        refresh_expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token_entity = RefreshToken(
            token_value=refresh_token_value,
            user_id=user.id,
            expires_at=refresh_expires_at,
        )

        try:
            saved_refresh_token = self.token_repo.add(refresh_token_entity)
            logger.info(f"Refresh token created for user {user.id}")
        except Exception as e:
            logger.error(f"Failed to save refresh token to DB for user {user.id}: {e}", exc_info=True)
            raise AuthenticationError("Could not save refresh token") from e

        return TokenResponseSchema(
            access_token=access_token,
            refresh_token=saved_refresh_token.token_value,
            token_type="bearer",
        )

    def login_user(self, email: str, password: str) -> TokenResponseSchema:
        """Authenticates a user and returns access/refresh tokens."""
        user = self.user_repo.get_by_email(email=email)

        if not user:
            logger.warning(f"Login attempt failed: User not found - {email}")
            raise AuthenticationError("Incorrect email or password")

        if not verify_password(password, user.hashed_password):
            logger.warning(f"Login attempt failed: Incorrect password for user {email}")
            raise AuthenticationError("Incorrect email or password")

        if not user.is_active:
            logger.warning(f"Login attempt failed: Inactive user {email}")
            raise AuthorizationError("Inactive user")

        logger.info(f"User {email} logged in successfully.")
        return self._create_auth_tokens(user)


    def refresh_access_token(self, refresh_token_value: str) -> TokenResponseSchema:
        """Refreshes an access token using a valid refresh token."""
        refresh_token = self.token_repo.get_by_token_value(token_value=refresh_token_value)

        if not refresh_token:
            logger.warning("Refresh token attempt failed: Token not found.")
            raise AuthenticationError("Invalid refresh token")

        if not refresh_token.is_valid():
            if refresh_token.revoked_at:
                logger.warning(f"Refresh token attempt failed: Token revoked for user {refresh_token.user_id} at {refresh_token.revoked_at}.")
                raise AuthenticationError("Refresh token has been revoked")
            else: 
                logger.warning(f"Refresh token attempt failed: Token expired for user {refresh_token.user_id} at {refresh_token.expires_at}.")
                raise AuthenticationError("Refresh token has expired")


        user = self.user_repo.get(id=refresh_token.user_id)
        if not user or not user.is_active:
             logger.warning(f"Refresh token attempt failed: User {refresh_token.user_id} not found or inactive.")
             # Revoke the potentially compromised token
             refresh_token.revoke()
             self.token_repo.update(refresh_token)
             raise AuthenticationError("User not found or inactive")

        refresh_token.revoke()
        try:
            self.token_repo.update(refresh_token)
            logger.info(f"Old refresh token {refresh_token.id} revoked for user {user.id}")
        except Exception as e:
             logger.error(f"Failed to update old refresh token {refresh_token.id} as revoked: {e}", exc_info=True)

        new_tokens = self._create_auth_tokens(user)
        logger.info(f"Tokens refreshed successfully for user {user.email}")
        return new_tokens


    def logout_user(self, refresh_token_value: str) -> None:
        """Logs out a user by revoking their refresh token."""
        refresh_token = self.token_repo.get_by_token_value(token_value=refresh_token_value)

        if refresh_token and not refresh_token.revoked_at:
            refresh_token.revoke()
            try:
                self.token_repo.update(refresh_token)
                logger.info(f"Refresh token {refresh_token.id} for user {refresh_token.user_id} revoked via logout.")
            except Exception as e:
                logger.error(f"Failed to update refresh token {refresh_token.id} as revoked during logout: {e}", exc_info=True)
        elif refresh_token:
             logger.warning(f"Logout attempt with already revoked token {refresh_token.id}")
        else:
             logger.warning("Logout attempt with non-existent refresh token value.")
