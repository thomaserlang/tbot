from enum import Enum


class TProvider(str, Enum):
    twitch = 'twitch'
    youtube = 'youtube'
    spotify = 'spotify'
    discord = 'discord'
