import datetime

from sqlalchemy import Boolean, Date, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.sql_alchemy.models.base import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=False, index=True
    )
