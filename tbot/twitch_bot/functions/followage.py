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
    data = await utils.twitch_request(bot.ahttp, 
        'https://api.twitch.tv/helix/users/follows',
        params={
            'from_id': uid,
            'to_id': channel_id,
        }
    )
    if not data['data']:
        raise Send_error('{} does not follow {}'.format(
            user, channel
        ))
    followed_at = parse(data['data'][0]['followed_at']).replace(tzinfo=None)
    seconds = (datetime.utcnow() - followed_at).total_seconds()

    return {
        'followage': utils.seconds_to_pretty(seconds),
        'followage_date': followed_at.strftime('%Y-%m-%d'),
        'followage_datetime': followed_at.strftime('%Y-%m-%d %H:%M:%S UTC'),
    }