import logging, urllib.parse
from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import utils

@fills_vars('subs')
async def subs(bot, channel_id, **kwargs):
    try:
        data = await utils.twitch_channel_token_request(
            bot, 
            channel_id,
            'https://api.twitch.tv/kraken/channels/{}/subscriptions?limit=1'.format(
                channel_id
            ),
        )
        return {
            'subs': data['_total'],
        }
    except utils.Twitch_request_error as e:
        raise Send_error('Unable to subs. Error: {}'.format(str(e)))