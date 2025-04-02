from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.interfaces.user_repository import IUserRepository
from app.infrastructure.database.sql_alchemy.models.user import User as UserModel
from app.infrastructure.repositories.sql_alchemy.base import SQLAlchemyBaseRepository


class SQLAlchemyUserRepository(
    SQLAlchemyBaseRepository[UserModel, User], IUserRepository
):
    """SQLAlchemy implementation of the User Repository interface."""
    def __init__(self, db: Session):
        super().__init__(db, UserModel, User)

    def get_by_email(self, *, email: str) -> Optional[User]:
        db_obj = self.db.query(self.model).filter(self.model.email == email).first()
        return self._to_entity(db_obj)

    def _create_entity_instance(self, db_obj: UserModel) -> User:
        return User(
            email=db_obj.email,
            hashed_password=db_obj.hashed_password,
            is_active=db_obj.is_active,
            is_superuser=db_obj.is_superuser,
        )

    def _from_entity(self, entity: User) -> UserModel:
        return UserModel(
            id=getattr(entity, "id", None),
            email=entity.email,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
        )
