from datetime import datetime, timezone
import logging
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_, update as sqlalchemy_update, delete as sqlalchemy_delete

from app.domain.entities.auth import RefreshToken
from app.domain.interfaces.token_repository import ITokenRepository
from app.infrastructure.database.sql_alchemy.models.token import RefreshTokenModel

logger = logging.getLogger(__name__)
class SQLAlchemyTokenRepository(ITokenRepository):
    """SQLAlchemy implementation for managing RefreshToken persistence."""
    def __init__(self, db: Session):
        self.db = db
        self.model = RefreshTokenModel
        self.entity_cls = RefreshToken

    def _to_entity(self, db_obj: Optional[RefreshTokenModel]) -> Optional[RefreshToken]:
        if db_obj is None:
            return None
        created_at = db_obj.created_at.replace(tzinfo=timezone.utc) if db_obj.created_at.tzinfo is None else db_obj.created_at
        expires_at = db_obj.expires_at.replace(tzinfo=timezone.utc) if db_obj.expires_at.tzinfo is None else db_obj.expires_at
        revoked_at = None
        if db_obj.revoked_at:
            revoked_at = db_obj.revoked_at.replace(tzinfo=timezone.utc) if db_obj.revoked_at.tzinfo is None else db_obj.revoked_at

        return self.entity_cls(
            id=db_obj.id,
            token_value=db_obj.token_value,
            user_id=db_obj.user_id,
            expires_at=expires_at,
            created_at=created_at,
            revoked_at=revoked_at,
        )

    def _from_entity(self, entity: RefreshToken) -> RefreshTokenModel:
        created_at_naive = entity.created_at.astimezone(timezone.utc).replace(tzinfo=None)
        expires_at_naive = entity.expires_at.astimezone(timezone.utc).replace(tzinfo=None)
        revoked_at_naive = None
        if entity.revoked_at:
            revoked_at_naive = entity.revoked_at.astimezone(timezone.utc).replace(tzinfo=None)

        return self.model(
            id=entity.id,
            token_value=entity.token_value,
            user_id=entity.user_id,
            expires_at=expires_at_naive,
            created_at=created_at_naive,
            revoked_at=revoked_at_naive,
        )

    def add(self, entity: RefreshToken) -> RefreshToken:
        db_obj = self._from_entity(entity)
        db_obj.id = None
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return self._to_entity(db_obj)

    def get_by_token_value(self, token_value: str) -> Optional[RefreshToken]:
        db_obj = self.db.query(self.model).filter(self.model.token_value == token_value).first()
        return self._to_entity(db_obj)


    def update(self, entity: RefreshToken) -> RefreshToken:
        if entity.id is None:
            raise ValueError("Cannot update entity without an ID")

        update_data = {
            "revoked_at": entity.revoked_at.astimezone(timezone.utc).replace(tzinfo=None) if entity.revoked_at else None,
            "expires_at": entity.expires_at.astimezone(timezone.utc).replace(tzinfo=None),
        }

        stmt = (
            sqlalchemy_update(self.model)
            .where(self.model.id == entity.id)
            .values(**update_data)
        )
        self.db.execute(stmt)

        self.db.commit()

        updated_db_obj = self.db.get(self.model, entity.id)


        if updated_db_obj is None:
             raise ValueError(f"Refresh token with ID {entity.id} not found after update attempt.")

        return self._to_entity(updated_db_obj)
    
    def remove_expired_or_revoked(self) -> int:
        """
        Removes refresh tokens that are either expired or have been revoked.
        Returns the number of tokens deleted.
        TODO: schedules cleaning ? But don't know how in that stack for now
        """
        now_utc_naive = datetime.now(timezone.utc)

        delete_condition = or_(
            self.model.revoked_at != None,
            self.model.expires_at <= now_utc_naive
        )

        # Build the delete statement
        stmt = sqlalchemy_delete(self.model).where(delete_condition)


        result = self.db.execute(stmt)
        self.db.commit()

        # Return the number of rows affected
        count = result.rowcount
        if count > 0:
             logger.info(f"Removed {count} expired/revoked refresh tokens.")
        return count
