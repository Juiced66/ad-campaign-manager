from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Token(BaseModel):
    """Schema for returning access and refresh tokens to the client."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    """Schema for requesting a token refresh."""
    refresh_token: str

class TokenInDB(BaseModel):
    """Schema representing token data as stored (potentially)."""
    token: str
    user_id: int
    created_at: datetime
    expires_at: datetime
    revoked_at: Optional[datetime] = None
