from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import utils
from datetime import datetime
from dateutil.parser import parse

@fills_vars('accountage', 'accountage_date', 'accountage_datetime')
async def accountage(bot, user_id, display_name, args, **kwargs):
    uid = user_id
    user = display_name
    if len(args) > 0:
        user = utils.safe_username(args[0])
        uid = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, user)
        if not uid:
            uid = user_id
            user = display_name
    data = await utils.twitch_request(bot.ahttp, 
        'https://api.twitch.tv/kraken/users/{}'.format(uid),
    )
    if not data:
        raise Send_error('Found no data on {}'.format(
            user,
        ))
    created_at = parse(data['created_at']).replace(tzinfo=None)
    seconds = (datetime.utcnow() - created_at).total_seconds()

    return {
        'accountage': utils.seconds_to_pretty(seconds),
        'accountage_date': created_at.strftime('%Y-%m-%d'),
        'accountage_datetime': created_at.strftime('%Y-%m-%d %H:%M:%S UTC'),
    }