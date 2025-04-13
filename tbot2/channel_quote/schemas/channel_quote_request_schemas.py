from typing import Annotated

from pydantic import StringConstraints, field_validator

from tbot2.common import BaseRequestSchema, Provider


class ChannelQuoteCreate(BaseRequestSchema):
    message: Annotated[str, StringConstraints(min_length=1, max_length=500)]
    provider: Provider
    created_by_chatter_id: Annotated[
        str, StringConstraints(min_length=0, max_length=36)
    ]
    created_by_display_name: Annotated[
        str, StringConstraints(min_length=1, max_length=200)
    ]


class ChannelQuoteUpdate(BaseRequestSchema):
    message: Annotated[str, StringConstraints(min_length=1, max_length=500)] | None = (
        None
    )
    provider: Provider | None = (
        None
    )
    created_by_chatter_id: (
        Annotated[str, StringConstraints(min_length=1, max_length=36)] | None
    ) = None
    created_by_display_name: (
        Annotated[str, StringConstraints(min_length=1, max_length=200)] | None
    ) = None

    @field_validator(
        'message',
        'provider',
        'created_by_chatter_id',
        'created_by_display_name',
    )
    def check_not_none(cls, v: str | None) -> str:
        if v is None:
            raise ValueError('Field cannot be None')
        return v
