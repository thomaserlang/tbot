from tbot2.channel_points import (
    get_channel_point_settings,
)
from tbot2.common import ChatMessage

from ..types import Command, TMessageVars
from ..var_filler import fills_vars


@fills_vars(
    provider='all',
    vars=('points_name',),
)
async def points_name_vars(
    chat_message: ChatMessage, command: Command, vars: TMessageVars
):
    settings = await get_channel_point_settings(channel_id=chat_message.channel_id)

    vars['points_name'].value = settings.points_name
