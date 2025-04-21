from tbot2.common import ChatMessage
from tbot2.twitch import (
    ModifyChannelInformationRequest,
    get_twitch_channel_information,
    get_twitch_game,
    update_twitch_channel_information,
)

from ..exceptions import CommandSyntaxError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(
    provider='twitch',
    vars=('set_game', 'set_category'),
)
async def change_twitch_category_vars(
    chat_message: ChatMessage, command: TCommand, vars: MessageVars
) -> None:
    name = ' '.join(command.args)
    if not name and vars['set_game'].args:
        name = ' '.join(vars['set_game'].args)
    if not name and vars['set_category'].args:
        name = ' '.join(vars['set_category'].args)

    if not name:
        raise CommandSyntaxError(
            f'No category provided. Usage: !{command.name} <category>'
        )
    game = await get_twitch_game(
        name=name,
    )
    if not game:
        raise CommandSyntaxError(f'No category found for: {name}')
    await update_twitch_channel_information(
        channel_id=chat_message.channel_id,
        broadcaster_id=chat_message.provider_id or '',
        data=ModifyChannelInformationRequest(
            game_id=game.id,
        ),
    )
    vars['set_game'].value = game.name
    vars['set_category'].value = game.name


@fills_vars(
    provider='twitch',
    vars=('game', 'category'),
)
async def get_twitch_category_vars(
    chat_message: ChatMessage, command: TCommand, vars: MessageVars
) -> None:
    channel = await get_twitch_channel_information(
        channel_id=chat_message.channel_id,
        broadcaster_id=chat_message.provider_id or '',
    )
    if channel:
        vars['game'].value = channel.game_name
        vars['category'].value = channel.game_name
