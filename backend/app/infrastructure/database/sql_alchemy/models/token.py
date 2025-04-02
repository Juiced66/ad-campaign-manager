from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.sql_alchemy.models.base import Base


class Token(Base):
    """SQLAlchemy model representing the 'tokens' table for auth tracking."""
    __tablename__ = "tokens"

    token: Mapped[str] = mapped_column(String, index=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    revoked_at: Mapped[datetime] = mapped_column(nullable=True)
