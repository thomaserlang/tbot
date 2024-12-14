from typing import Literal

from pydantic import BaseModel


class TwitchBadge(BaseModel):
    set_id: str
    id: str
    info: str


class TwitchFragmentEmote(BaseModel):
    id: str
    emote_set_id: str
    owner_id: str
    format: list[Literal['animated', 'static'] | str]


class TwitchFragmentCheermote(BaseModel):
    prefix: str
    bits: int
    tier: int


class TwitchFragmentMention(BaseModel):
    user_id: str
    user_login: str
    user_name: str


class TwitchMessageFragment(BaseModel):
    type: Literal['text', 'emote', 'cheermote', 'mention'] | str
    text: str
    cheermote: TwitchFragmentCheermote | None
    emote: TwitchFragmentEmote | None
    mention: TwitchFragmentMention | None
