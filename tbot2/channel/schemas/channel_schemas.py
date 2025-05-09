from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints, computed_field, field_validator

from tbot2.common import (
    FEATURES_BY_SUBSCRIPTION,
    BaseRequestSchema,
    BaseSchema,
    Feature,
    SubscriptionType,
)


class ChannelCreate(BaseRequestSchema):
    display_name: Annotated[str, StringConstraints(min_length=1, max_length=200)]


class ChannelUpdate(BaseRequestSchema):
    display_name: (
        Annotated[str, StringConstraints(min_length=1, max_length=200)] | None
    ) = None

    @field_validator('display_name')
    def check_not_none(cls, value: str | bool | None) -> str | bool:
        if value is None:
            raise ValueError('Must not be None')
        return value


class Channel(BaseSchema):
    id: UUID
    display_name: str
    created_at: datetime
    subscription: SubscriptionType | None

    @computed_field
    @property
    def features(self) -> set[Feature]:
        if self.subscription:
            return FEATURES_BY_SUBSCRIPTION.get(
                self.subscription,
                set(),
            )
        return set()
