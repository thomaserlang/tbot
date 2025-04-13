from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints, field_validator

from tbot2.common import BaseRequestSchema, BaseSchema

from ..types import BannedTermType


class BannedTerm(BaseSchema):
    id: UUID
    chat_filter_id: UUID
    type: BannedTermType
    text: str


class BannedTermCreate(BaseRequestSchema):
    type: BannedTermType
    text: Annotated[str, StringConstraints(min_length=1, max_length=1000)]


class BannedTermUpdate(BaseRequestSchema):
    type: BannedTermType | None = None
    text: Annotated[str, StringConstraints(min_length=1, max_length=1000)] | None = None

    @field_validator('type', 'text')
    @classmethod
    def check_not_none(cls, v: str | bool | None) -> str | bool:
        if v is None:
            raise ValueError('Field cannot be None')
        return v


class BannedTermTest(BaseRequestSchema):
    message: Annotated[str, StringConstraints(min_length=1, max_length=1000)]