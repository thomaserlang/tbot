import logging, urllib.parse
from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import utils

@fills_vars('subs')
async def subs(bot, channel_id, **kwargs):
    try:
        data = await utils.twitch_channel_token_request(
            bot, 
            channel_id,
            'https://api.twitch.tv/subscriptions',
            params={'broadcaster_id': channel_id}
        )
        return {
            'subs': data['total'],
        }
    except utils.Twitch_request_error as e:
        raise Send_error('Unable to get sub count. Error: {}'.format(str(e)))