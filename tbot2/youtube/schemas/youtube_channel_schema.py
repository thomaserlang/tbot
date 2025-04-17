
from tbot2.common import BaseSchema


class YoutubeChannelSnippet(BaseSchema):
    title: str


class YoutubeChannel(BaseSchema):
    id: str
    snippet: YoutubeChannelSnippet

