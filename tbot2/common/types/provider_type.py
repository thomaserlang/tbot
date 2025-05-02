from typing import Literal

Provider = Literal[
    'twitch',
    'discord',
    'youtube',
    'spotify',
    'tiktok',
]

channel_provider_scopes: dict[Provider, str] = {}
bot_provider_scopes: dict[Provider, str] = {}
