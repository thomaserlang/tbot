from enum import StrEnum


class TProvider(StrEnum):
    twitch = 'twitch'
    youtube = 'youtube'
    spotify = 'spotify'
    discord = 'discord'


channel_provider_scopes: dict[TProvider, str] = {}
bot_provider_scopes: dict[TProvider, str] = {}
