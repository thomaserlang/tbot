from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import utils
from datetime import datetime
from dateutil.parser import parse

@fills_vars('followage', 'followage_date', 'followage_datetime')
async def followage(bot, user_id, display_name, channel_id, channel, args, **kwargs):
    uid = user_id
    user = display_name
    if len(args) > 0:
        user = utils.safe_username(args[0])
        uid = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, user)
        if not uid:
            uid = user_id
            user = display_name
    data = await utils.twitch_channel_token_request(bot, channel_id,
        'https://api.twitch.tv/helix/channels/followers',
        params={
            'user_id': uid,
            'broadcaster_id': channel_id,
        }
    )
    if not data['data']:
        raise Send_error(f'{user} does not follow {channel}')
    followed_at = parse(data['data'][0]['followed_at']).replace(tzinfo=None)

    return {
        'followage': utils.seconds_to_pretty(dt1=datetime.utcnow(), dt2=followed_at),
        'followage_date': followed_at.strftime('%Y-%m-%d'),
        'followage_datetime': followed_at.strftime('%Y-%m-%d %H:%M:%S UTC'),
    }