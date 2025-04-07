from enum import StrEnum


class TProvider(StrEnum):
    twitch = 'twitch'
    youtube = 'youtube'
    spotify = 'spotify'
    discord = 'discord'


provider_scopes: dict[TProvider, str] = {}
