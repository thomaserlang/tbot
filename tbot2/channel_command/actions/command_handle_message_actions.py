import sys
from dataclasses import dataclass
from uuid import UUID

from async_lru import alru_cache
from loguru import logger

from tbot2.bot_providers import BotProvider
from tbot2.channel import get_channel_bot_provider
from tbot2.channel_stream import get_current_channel_provider_stream
from tbot2.common import ChatMessage, check_pattern_match
from tbot2.contexts import AsyncSession, get_session
from tbot2.exceptions import ErrorMessage

from ..exceptions import CommandError
from ..fill_message import fill_message
from ..types import TCommand
from .command_actions import Command, get_commands


@dataclass
class MessageResponse:
    command: Command
    response: str
    bot_provider: BotProvider | None = None


async def handle_message_response(
    chat_message: ChatMessage,
    session: AsyncSession | None = None,
) -> MessageResponse | None:
    async with get_session(session) as session:
        commands = await get_cached_commands(
            channel_id=chat_message.channel_id,
            session=session,
        )
        # Bail early if there are no patterns or cmds to match
        has_patters = any(command.patterns for command in commands)
        if not has_patters and not chat_message.message.startswith('!'):
            return None

        for command in commands:
            if command.enabled is False:
                continue
            if command.access_level > chat_message.access_level:
                continue
            if command.provider != 'all' and command.provider != chat_message.provider:
                continue
            if not await _check_active_mode(
                command=command,
                chat_message=chat_message,
                session=session,
            ):
                continue

            if response := await _matches_command(chat_message, command):
                response.bot_provider = await get_channel_bot_provider(
                    provider=chat_message.provider,
                    channel_id=chat_message.channel_id,
                    session=session,
                )
                if response.bot_provider:
                    # Check that the bot is not replying to itself
                    # causing an infinite loop
                    if (
                        response.bot_provider.provider_user_id
                        == chat_message.provider_viewer_id
                    ):
                        logger.debug('Bot is replying to itself, skipping')
                        return None
                return response
            else:
                logger.trace(f'No matched command for message: {chat_message.message}')

    return None


async def _check_active_mode(
    command: Command,
    chat_message: ChatMessage,
    session: AsyncSession,
) -> bool:
    if command.active_mode == 'always':
        return True
    stream = await get_current_channel_provider_stream(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        session=session,
    )
    if command.active_mode == 'offline' and stream:
        return False
    if command.active_mode == 'online' and not stream:
        return False
    return True


async def _matches_command(
    chat_message: ChatMessage, command: Command
) -> MessageResponse | None:
    if chat_message.message.startswith('!'):
        return await _matches_cmd(chat_message, command)

    return await _matches_pattern(chat_message, command)


async def _matches_cmd(
    chat_message: ChatMessage, command: Command
) -> MessageResponse | None:
    args = chat_message.message[1:].split(' ')
    cmd = args.pop(0).lower()
    if cmd not in command.cmds:
        return None
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
    except ErrorMessage as e:
        return MessageResponse(
            response=str(e),
            command=command,
        )


async def _matches_pattern(
    chat_message: ChatMessage, command: Command
) -> MessageResponse | None:
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
async def get_cached_commands(
    channel_id: UUID, session: AsyncSession | None = None
) -> list[Command]:
    return await get_commands(
        channel_id=channel_id,
        session=session,
    )
