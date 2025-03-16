from dataclasses import dataclass
from typing import Awaitable, Callable, Sequence

from tbot2.common import ChatMessage, TProvider, TScope


@dataclass(slots=True)
class TMessageVar:
    name: str
    match_raw: str
    args: Sequence[str]
    value: str | int | None = None
    found: bool = False


@dataclass(slots=True)
class TCommand:
    name: str
    args: Sequence[str]


@dataclass(slots=True)
class TFillVars:
    provider: str | TProvider
    vars: Sequence[str]


TMessageVars = dict[str, TMessageVar]
TFillerType = Callable[[ChatMessage, TCommand, TMessageVars], Awaitable[None]]


class TCommandScope(TScope):
    READ = 'command:read'
    WRITE = 'command:write'
