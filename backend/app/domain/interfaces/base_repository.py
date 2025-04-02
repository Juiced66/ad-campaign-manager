from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

EntityType = TypeVar("EntityType")


class IRepository(Generic[EntityType], ABC):
    @abstractmethod
    def get(self, id: Any) -> Optional[EntityType]: ...

    @abstractmethod
    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[EntityType]: ...

    @abstractmethod
    def create(self, *, entity: EntityType) -> EntityType: ...

    @abstractmethod
    def update(self, *, id: Any, entity: EntityType) -> EntityType: ...

    @abstractmethod
    def remove(self, *, id: Any) -> Optional[EntityType]: ...
