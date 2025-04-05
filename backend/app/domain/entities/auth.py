from datetime import datetime, timezone


class AccessTokenData:
    """Represents access token details within the domain."""
    def __init__(
        self,
        access_token: str,
        user_id: int,
        expires_at: datetime,
        created_at: datetime | None = None,
    ):
        self.access_token = access_token
        self.user_id = user_id
        self.expires_at = expires_at
        self.created_at = created_at or datetime.now(timezone.utc)

    def is_expired(self) -> bool:
        """Checks if the access token is expired."""
        return datetime.now(timezone.utc) >= self.expires_at


class RefreshToken:
    """Represents a refresh token within the domain."""
    def __init__(
        self,
        token_value: str,
        user_id: int,
        expires_at: datetime,
        created_at: datetime | None = None,
        revoked_at: datetime | None = None,
        id: int | None = None,
    ):
        self.id = id
        self.token_value = token_value
        self.user_id = user_id
        self.expires_at = expires_at
        self.created_at = created_at or datetime.now(timezone.utc)
        self.revoked_at = revoked_at

    def is_valid(self) -> bool:
        """Checks if the refresh token is currently valid (not revoked, not expired)."""
        return self.revoked_at is None and datetime.now(timezone.utc) < self.expires_at

    def revoke(self) -> None:
        """Marks the token as revoked."""
        if not self.revoked_at:
            self.revoked_at = datetime.now(timezone.utc)
