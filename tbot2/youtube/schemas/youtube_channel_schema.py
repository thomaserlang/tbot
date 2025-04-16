from typing import Generic, TypeVar

from tbot2.common import BaseSchema


class YoutubeChannelSnippet(BaseSchema):
    title: str


class YoutubeChannel(BaseSchema):
    id: str
    snippet: YoutubeChannelSnippet


T = TypeVar('T')


class YoutubeItems(BaseSchema, Generic[T]):
    items: list[T]
