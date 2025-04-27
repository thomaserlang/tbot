from typing import Annotated, Any, Generic, TypeVar

from fastapi import Depends
from pydantic import BaseModel, Field

T = TypeVar('T')


class PageCursorQuery(BaseModel):
    cursor: str | None = None
    per_page: Annotated[int, Field(ge=1, le=100)] = 25


PageCursorQueryDep = Annotated[PageCursorQuery, Depends()]


class PageCursor(BaseModel, Generic[T]):
    records: list[T]
    lookup_data: dict[str, dict[str, Any]] = {}
    cursor: str | None = None
    total: int | None = None
