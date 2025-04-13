from typing import Literal

Provider = Literal[
    'twitch',
    'discord',
    'youtube',
    'spotify',
]

channel_provider_scopes: dict[Provider, str] = {}
bot_provider_scopes: dict[Provider, str] = {}
