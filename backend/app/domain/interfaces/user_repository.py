from abc import abstractmethod
from typing import Optional

from app.domain.entities.user import User
from app.domain.interfaces.base_repository import IRepository


class IUserRepository(IRepository[User]):
    """Interface for User data persistence operations."""
    @abstractmethod
    def get_by_email(self, *, email: str) -> Optional[User]:
        """Retrieves a user by their email address."""
