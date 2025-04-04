from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response for requests"""
    items: List[T]
    total: int
