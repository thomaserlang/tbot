from tbot2.common import ChatMessageCreate
from tbot2.twitch import (
    ModifyChannelInformationRequest,
    get_twitch_channel_information,
    update_twitch_channel_information,
)

from ..exceptions import CommandSyntaxError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(
    provider='twitch',
    vars=('set_title',),
)
async def change_twitch_title_vars(
    chat_message: ChatMessageCreate, command: TCommand, vars: MessageVars
) -> None:
    title = ' '.join(command.args)
    if not title and vars['set_title'].args:
        title = ' '.join(vars['set_title'].args)
    if not title:
        raise CommandSyntaxError(f'No title provided. Usage: !{command.name} <title>')
    await update_twitch_channel_information(
        channel_id=chat_message.channel_id,
        broadcaster_id=chat_message.provider_channel_id or '',
        data=ModifyChannelInformationRequest(
            title=title[:140],
        ),
    )
    vars['set_title'].value = title[:140]


@fills_vars(
    provider='twitch',
    vars=('title',),
)
async def get_twitch_title_vars(
    chat_message: ChatMessageCreate, command: TCommand, vars: MessageVars
) -> None:
    channel = await get_twitch_channel_information(
        channel_id=chat_message.channel_id,
        broadcaster_id=chat_message.provider_channel_id or '',
    )
    if channel:
        vars['title'].value = channel.title
