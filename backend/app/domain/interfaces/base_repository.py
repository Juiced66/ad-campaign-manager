from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

EntityType = TypeVar("EntityType")


class IRepository(Generic[EntityType], ABC):
    """Generic interface for basic CRUD operations on domain entities."""
    @abstractmethod
    def get(self, id: Any) -> Optional[EntityType]:
        """Retrieves a single entity by its identifier."""

    @abstractmethod
    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[EntityType]:
        """Retrieves multiple entities with pagination."""

    @abstractmethod
    def create(self, *, entity: EntityType) -> EntityType:
        """Creates a new entity."""

    @abstractmethod
    def update(self, *, id: Any, entity: EntityType) -> EntityType:
        """Updates an existing entity identified by its ID."""

    @abstractmethod
    def remove(self, *, id: Any) -> Optional[EntityType]:
        """Removes an entity by its identifier."""
