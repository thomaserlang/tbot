from dataclasses import dataclass
from typing import Awaitable, Callable, Sequence

from tbot2.common import ChatMessage

__all__ = [
    'MessageVar',
    'Command',
    'TMessageVars',
    'TFillerType',
]


@dataclass(slots=True)
class MessageVar:
    name: str
    match_raw: str
    args: Sequence[str]
    value: str | int | None = None
    found: bool = False


@dataclass(slots=True)
class Command:
    name: str
    args: Sequence[str]


@dataclass(slots=True)
class FillVars:
    provider: str
    vars: Sequence[str]


TMessageVars = dict[str, MessageVar]
TFillerType = Callable[[ChatMessage, Command, TMessageVars], Awaitable[None]]
