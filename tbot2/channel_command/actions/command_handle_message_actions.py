import sys
from dataclasses import dataclass
from uuid import UUID

from async_lru import alru_cache

from tbot2.common import ChatMessage, check_pattern_match
from tbot2.contexts import AsyncSession

from ..exceptions import CommandError
from ..fill_message import fill_message
from ..types import TCommand
from .command_actions import Command, get_commands


@dataclass
class MessageResponse:
    command: Command
    response: str


async def handle_message_response(
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
            args = chat_message.message[1:].split(' ')
            cmd = args.pop(0).lower()
            if cmd not in command.cmds:
                continue
            try:
                response = await fill_message(
                    response_message=command.response,
                    command=TCommand(
                        name=cmd,
                        args=args,
                    ),
                    chat_message=chat_message,
                )
                return MessageResponse(response=response, command=command)
            except CommandError as e:
                return MessageResponse(
                    response=str(e),
                    command=command,
                )

        else:
            for pattern in command.patterns:
                if not check_pattern_match(chat_message.message, pattern):
                    continue
                try:
                    response = await fill_message(
                        response_message=command.response,
                        command=TCommand(
                            name='pattern',
                            args=[],
                        ),
                        chat_message=chat_message,
                    )
                    return MessageResponse(response=response, command=command)
                except CommandError as e:
                    return MessageResponse(
                        response=str(e),
                        command=command,
                    )
    return None


@alru_cache(ttl=2, maxsize=1000 if 'pytest' not in sys.modules else 0)
async def get_cached_commands(channel_id: UUID, session: AsyncSession | None = None):
    return await get_commands(
        channel_id=channel_id,
        session=session,
    )
