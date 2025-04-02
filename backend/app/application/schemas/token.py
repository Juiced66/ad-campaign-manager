from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenInDB(BaseModel):
    token: str
    user_id: int
    created_at: datetime
    revoked_at: Optional[datetime] = None
