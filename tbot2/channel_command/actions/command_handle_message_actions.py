import shlex
import sys
from dataclasses import dataclass
from re import IGNORECASE, search
from uuid import UUID

from async_lru import alru_cache

from tbot2.common import ChatMessage
from tbot2.contexts import AsyncSession

from ..types import TCommand
from ..var_filler import fill_message
from .command_actions import Command, get_commands


@dataclass
class MessageResponse:
    command: Command
    response: str


async def handle_message(
    chat_message: ChatMessage,
    session: AsyncSession | None = None,
) -> MessageResponse | None:
    commands = await get_cached_commands(
        channel_id=chat_message.channel_id,
        session=session,
    )

    for command in commands:
        if command.enabled is False:
            continue
        if command.access_level > chat_message.access_level:
            continue
        if command.provider != 'all' and command.provider != chat_message.provider:
            continue

        if chat_message.message.startswith('!'):
            cmd = chat_message.message[1:].lower()
            if cmd in command.cmds:
                response = await fill_message(
                    response_message=command.response,
                    command=TCommand(
                        name=cmd,
                        args=chat_message.message[len(cmd) + 1 :].strip().split(' '),
                    ),
                    chat_message=chat_message,
                )
                return MessageResponse(response=response, command=command)
        else:
            for pattern in command.patterns:
                if check_pattern_match(chat_message, pattern):
                    response = await fill_message(
                        response_message=command.response,
                        command=TCommand(
                            name='pattern',
                            args=[],
                        ),
                        chat_message=chat_message,
                    )
                    return MessageResponse(response=response, command=command)

    return None


@alru_cache(ttl=2, maxsize=1000 if 'pytest' not in sys.modules else 0)
async def get_cached_commands(channel_id: UUID, session: AsyncSession | None = None):
    return await get_commands(
        channel_id=channel_id,
        session=session,
    )


def check_pattern_match(chat_message: ChatMessage, pattern: str) -> bool:
    if pattern.startswith('re:'):
        if search(
            pattern[3:],
            chat_message.message_without_fragments(),
            flags=IGNORECASE,
        ):
            return True
    else:
        split = pattern.split(' ') if '"' not in pattern else shlex.split(pattern)
        if all(
            [
                search(
                    rf'\b{s}\b',
                    chat_message.message_without_fragments(),
                    flags=IGNORECASE,
                )
                for s in split
            ]
        ):
            return True
    return False
