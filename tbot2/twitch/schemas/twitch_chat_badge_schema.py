from tbot2.common import BaseSchema


class ChatBadgeVersion(BaseSchema):
    id: str
    description: str
    title: str
    image_url_1x: str
    image_url_2x: str
    image_url_4x: str
    click_action: str | None = None
    click_url: str | None = None


class ChatBadge(BaseSchema):
    set_id: str
    versions: list[ChatBadgeVersion]


class ChannelBadges(BaseSchema):
    channel_badges: list[ChatBadge]
    global_badges: list[ChatBadge]