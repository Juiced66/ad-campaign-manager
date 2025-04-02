from abc import ABC, abstractmethod


class ITokenRepository(ABC):
    """Token Repository Interface"""

    @abstractmethod
    def save_token(self, token: str, user_id: int) -> None:
        """Persists a token for a given user."""

    @abstractmethod
    def revoke_token(self, token: str) -> None:
        """Revokes a given token."""

    @abstractmethod
    def token_exists(self, token: str) -> bool:
        """Checks if a token is revoked or not found."""
