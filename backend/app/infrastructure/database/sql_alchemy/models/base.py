from sqlalchemy import Integer
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base for all SQLAlchemy models."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Helper method to convert model instance to dictionary
    def as_dict(self) -> dict[str, any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
