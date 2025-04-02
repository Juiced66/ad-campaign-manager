from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Schema for returning an access token to the client."""
    access_token: str
    token_type: str = "bearer"


class TokenInDB(BaseModel):
    """Schema representing token data as stored (potentially)."""
    token: str
    user_id: int
    created_at: datetime
    revoked_at: Optional[datetime] = None
