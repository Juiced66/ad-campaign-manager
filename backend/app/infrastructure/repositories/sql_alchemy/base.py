from abc import abstractmethod
from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from app.domain.interfaces.base_repository import IRepository

ModelType = TypeVar("ModelType")
EntityType = TypeVar("EntityType")


class SQLAlchemyBaseRepository(Generic[ModelType, EntityType], IRepository[EntityType]):
    def __init__(
        self, db: Session, model: Type[ModelType], entity_cls: Type[EntityType]
    ):
        self.db = db
        self.model = model
        self.entity_cls = entity_cls

    @abstractmethod
    def _create_entity_instance(self, db_obj: ModelType) -> EntityType:
        raise NotImplementedError

    @abstractmethod
    def _from_entity(self, entity: EntityType) -> ModelType:
        raise NotImplementedError

    def _to_entity(self, db_obj: Optional[ModelType]) -> Optional[EntityType]:
        if db_obj is None:
            return None
        entity_instance = self._create_entity_instance(db_obj)
        entity_instance.id = db_obj.id
        return entity_instance

    def get(self, id: Any) -> Optional[EntityType]:
        db_obj = self.db.query(self.model).filter(self.model.id == id).first()
        return self._to_entity(db_obj)

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[EntityType]:
        db_objs = self.db.query(self.model).offset(skip).limit(limit).all()
        return [self._to_entity(obj) for obj in db_objs if obj is not None]

    def create(self, *, entity: EntityType) -> EntityType:
        db_obj = self._from_entity(entity)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return self._to_entity(db_obj)

    def update(self, *, id: Any, entity: EntityType) -> EntityType:
        db_obj = self.db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            raise ValueError(f"Entity with id {id} not found")

        update_model_instance = self._from_entity(entity)
        update_data = update_model_instance.__dict__

        update_data.pop("id", None)
        update_data.pop("_sa_instance_state", None)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        self.db.commit()
        self.db.refresh(db_obj)
        return self._to_entity(db_obj)

    def remove(self, *, id: Any) -> Optional[EntityType]:
        db_obj = self.db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            entity = self._to_entity(db_obj)
            self.db.delete(db_obj)
            self.db.commit()
            return entity
        return None
