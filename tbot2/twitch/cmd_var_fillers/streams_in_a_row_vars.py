from tbot2.channel_viewer_stats import get_channel_viewer_stats
from tbot2.command import TCommand, TMessageVars, fills_vars
from tbot2.common import ChatMessage, TProvider, safe_username

from ..actions.twitch_lookup_users_action import lookup_twitch_user


@fills_vars(
    provider=TProvider.twitch,
    vars=(
        'user.streams_row',
        'user.streams_total',
        'user.streams_row_peak',
        'user.streams_row_peak_date',
        'user.streams_row_text',
    ),
)
async def streams_in_a_row_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
):
    for_viewer_id = chat_message.chatter_id
    if len(command.args) > 0:
        chatter = await lookup_twitch_user(
            channel_id=chat_message.channel_id,
            login=safe_username(command.args[0]),
        )
        if not chatter:
            raise ValueError('User not found.')
        for_viewer_id = chatter.id

    stats = await get_channel_viewer_stats(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        viewer_id=for_viewer_id,
    )
    vars['user.streams_row'].value = stats.streams_row
    vars['user.streams_total'].value = stats.streams
    vars['user.streams_row_peak'].value = stats.streams_row_peak
    vars['user.streams_row_peak_date'].value = (
        stats.streams_row_peak_date.isoformat() if stats.streams_row_peak_date else None
    )
    vars[
        'user.streams_row_text'
    ].value = f'{chat_message.chatter_display_name} has been here for {stats.streams_row} in a row'
