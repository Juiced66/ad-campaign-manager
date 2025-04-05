from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.sql_alchemy.models.base import Base

class RefreshTokenModel(Base):
    """SQLAlchemy model representing the 'refresh_tokens' table."""
    __tablename__ = "refresh_tokens"

    token_value: Mapped[str] = mapped_column(String(255), index=True, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)