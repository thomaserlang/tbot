from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints, field_validator

from tbot2.common import BaseRequestSchema, BaseSchema

from ..types import TBannedTermType


class BannedTerm(BaseSchema):
    id: UUID
    chat_filter_id: UUID
    type: TBannedTermType
    text: str
    enabled: bool


class BannedTermCreate(BaseRequestSchema):
    type: TBannedTermType
    text: Annotated[str, StringConstraints(min_length=1, max_length=1000)]
    enabled: bool = True


class BannedTermUpdate(BaseRequestSchema):
    type: TBannedTermType | None = None
    text: Annotated[str, StringConstraints(min_length=1, max_length=1000)] | None = None
    enabled: bool | None = None

    @field_validator('type', 'text', 'enabed')
    @classmethod
    def check_not_none(cls, v: str | bool | None) -> str | bool:
        if v is None:
            raise ValueError('Field cannot be None')
        return v
