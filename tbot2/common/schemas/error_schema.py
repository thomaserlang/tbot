from typing import Any

from .base_schema import BaseSchema


class SubError(BaseSchema):
    field: str
    message: str
    type: str
    input: Any | None = None


class Error(BaseSchema):
    code: int
    message: str
    type: str
    errors: list[SubError]
