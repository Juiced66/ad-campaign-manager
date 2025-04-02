from datetime import datetime

from sqlalchemy.orm import Session

from app.domain.interfaces.token_repository import ITokenRepository
from app.infrastructure.database.sql_alchemy.models.token import Token as TokenModel


class SQLAlchemyTokenRepository(ITokenRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_token(self, token: str, user_id: int) -> None:
        db_token = TokenModel(token=token, user_id=user_id)
        self.db.add(db_token)
        self.db.commit()

    def revoke_token(self, token: str) -> None:
        db_token = self.db.query(TokenModel).filter(TokenModel.token == token).first()
        if db_token:
            db_token.revoked_at = datetime.utcnow()
            self.db.commit()

    def delete_token(self, token: str) -> None:
        db_token = self.db.query(TokenModel).filter(TokenModel.token == token).first()
        self.db.delete(db_token)
        self.db.commit()

    def token_exists(self, token: str) -> bool:
        db_token = self.db.query(TokenModel).filter(TokenModel.token == token).first()
        return db_token is None or db_token.revoked_at is not None
