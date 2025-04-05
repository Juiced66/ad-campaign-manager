from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.auth import RefreshToken

class ITokenRepository(ABC):
    """
    Token Repository Interface for managing persistent Refresh Tokens.
    """

    @abstractmethod
    def add(self, entity: RefreshToken) -> RefreshToken:
        """Persists a new refresh token entity."""
        pass

    @abstractmethod
    def get_by_token_value(self, token_value: str) -> Optional[RefreshToken]:
         """Retrieves a refresh token entity by its value."""
         pass

    @abstractmethod
    def update(self, entity: RefreshToken) -> RefreshToken:
        """Updates an existing refresh token entity (e.g., setting revoked_at)."""
        pass

    @abstractmethod
    def remove_expired_or_revoked(self) -> int:
       """Removes old tokens and returns the count removed."""
       pass