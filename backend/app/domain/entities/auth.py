from datetime import datetime, timezone


class AccessTokenData:
    """Represents access token details within the domain."""
    def __init__(
        self,
        access_token: str,
        user_id: int,
        expires_at: datetime,
        created_at: datetime = None,
    ):
        self.access_token = access_token
        self.user_id = user_id
        self.expires_at = expires_at
        self.created_at = created_at or datetime.now(timezone.utc)
