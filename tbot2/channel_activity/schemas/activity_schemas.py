from datetime import datetime
from typing import Annotated, Self
from uuid import UUID

from pydantic import (
    Field,
    StringConstraints,
    computed_field,
    field_validator,
    model_validator,
)
from pydantic_extra_types.currency_code import ISO4217
from uuid6 import uuid7

from tbot2.channel_activity.constants.activity_types_constants import (
    ACTIVITY_TYPE_NAMES_DICT,
)
from tbot2.common import (
    BaseRequestSchema,
    BaseSchema,
    ChatMessagePart,
    ChatMessagePartRequest,
    MentionPartRequest,
    Provider,
    datetime_now,
)
from tbot2.common.schemas.chat_message_schema import MentionPart

from ..types.activity_type import (
    ActivityId,
    ActivitySubType,
    ActivityType,
)


class ActivityCreate(BaseRequestSchema):
    id: ActivityId = Field(default_factory=lambda: ActivityId(uuid7()))
    channel_id: UUID
    type: Annotated[ActivityType | str, StringConstraints(min_length=0, max_length=255)]
    sub_type: Annotated[
        ActivitySubType | str, StringConstraints(min_length=0, max_length=255)
    ] = ''
    provider: Provider
    provider_message_id: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    provider_user_id: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    provider_viewer_id: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    viewer_name: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    viewer_display_name: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    count: int = 0
    count_decimal_place: int = 0
    count_currency: ISO4217 | None = None
    created_at: datetime = Field(default_factory=datetime_now)
    gifted_viewers: list[MentionPartRequest] | None = None
    system_message: Annotated[str, StringConstraints(min_length=0, max_length=2000)] = (
        ''
    )
    message: Annotated[str, StringConstraints(min_length=0, max_length=2000)] | None = (
        None
    )
    message_parts: list[ChatMessagePartRequest] | None = None
    read: bool = False

    @model_validator(mode='after')  # noqa: F821
    def message_default(self) -> Self:
        if self.message and not self.message_parts:
            self.message_parts = [
                ChatMessagePartRequest(
                    type='text',
                    text=self.message,
                )
            ]
        return self


class ActivityUpdate(BaseRequestSchema):
    gifted_viewers: list[MentionPartRequest] | None = None
    read: bool | None = None

    @field_validator('read')
    def check_not_null(cls, value: bool | None) -> bool:
        if value is None:
            raise ValueError('Cannot be null')
        return value


class Activity(BaseSchema):
    id: ActivityId
    channel_id: UUID
    provider: Provider
    provider_message_id: str
    provider_user_id: str
    provider_viewer_id: str
    viewer_name: str
    viewer_display_name: str
    type: ActivityType | str
    sub_type: ActivitySubType | str
    count: int
    count_decimal_place: int
    count_currency: str | None
    created_at: datetime
    gifted_viewers: list[MentionPart] | None = None
    system_message: str
    message: str | None = None
    message_parts: list[ChatMessagePart] | None = None
    read: bool

    @computed_field
    @property
    def color(self) -> str:
        if self.type not in ACTIVITY_TYPE_NAMES_DICT:
            return '#EFBF04'
        return ACTIVITY_TYPE_NAMES_DICT[self.type].color

    @computed_field
    @property
    def count_name(self) -> str:
        if self.type not in ACTIVITY_TYPE_NAMES_DICT:
            return ''
        return ACTIVITY_TYPE_NAMES_DICT[self.type].count_name

    @computed_field
    @property
    def type_display_name(self) -> str:
        if self.type not in ACTIVITY_TYPE_NAMES_DICT:
            return self.type
        return ACTIVITY_TYPE_NAMES_DICT[self.type].display_name

    @computed_field
    @property
    def sub_type_display_name(self) -> str:
        if self.type not in ACTIVITY_TYPE_NAMES_DICT:
            return self.sub_type
        if self.sub_type not in ACTIVITY_TYPE_NAMES_DICT[self.type].sub_type_names:
            return self.sub_type
        return ACTIVITY_TYPE_NAMES_DICT[self.type].sub_type_names[self.sub_type]
