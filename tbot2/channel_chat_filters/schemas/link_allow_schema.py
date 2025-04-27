from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints

from tbot2.common import BaseSchema


class LinkAllow(BaseSchema):
    id: UUID
    chat_filter_id: UUID
    url: str


class LinkAllowCreate(BaseSchema):
    url: Annotated[str, StringConstraints(min_length=1, max_length=1000)]


class LinkAllowUpdate(BaseSchema):
    url: Annotated[str, StringConstraints(min_length=1, max_length=1000)]
