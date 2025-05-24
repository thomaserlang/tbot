from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import Literal

from tbot2.common import ChatMessageCreate, Provider, Scope


@dataclass(slots=True)
class MessageVar:
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
class FillVars:
    provider: Provider | Literal['all']
    vars: Sequence[str]


MessageVars = dict[str, MessageVar]
FillerType = Callable[[ChatMessageCreate, TCommand, MessageVars], Awaitable[None]]


class CommandScope(Scope):
    READ = 'command:read'
    WRITE = 'command:write'


CommandActiveMode = Literal['always', 'online', 'offline']
