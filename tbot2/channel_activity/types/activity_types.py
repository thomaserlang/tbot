from dataclasses import dataclass, field
from typing import Literal, NewType
from uuid import UUID

from tbot2.common import Provider, Scope

ActivityId = NewType('ActivityId', UUID)

TwitchActivityType = Literal[
    'sub',
    'resub',
    'gift_sub',
    'community_sub_gift',
    'raid',
    'charity_donation',
    'bits',
    'follow',
    'points',
]
TwitchActivitySubType = Literal['prime', '1000', '2000', '3000']

YoutubeActivityType = Literal[
    'newSponsorEvent',
    'superChatEvent',
    'superStickerEvent',
    'membershipGiftingEvent',
    'memberMilestoneChatEvent',
]

TikTokActivityType = Literal['gift']


ActivityType = TwitchActivityType | YoutubeActivityType | TikTokActivityType


ActivitySubType = TwitchActivitySubType


class ActivityScope(Scope):
    READ = 'channel_activity:read'
    WRITE = 'channel_activity:write'


@dataclass(slots=True)
class ActivityTypeName:
    name: ActivityType
    display_name: str
    color: str
    provider: Provider
    count_name: str
    filter_min_count: bool = False
    sub_type_names: dict[str, str] = field(default_factory=lambda: {})
