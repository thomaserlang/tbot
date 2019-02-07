import logging
from tbot import config, utils
from tbot.twitch_bot.bot_main import bot
from .badge_log import badge_log

sub_mystery_gift = {}

@bot.on('USERNOTICE')
async def usernotice(**kwargs):

    # Prevent spamming the chat when mystery subs are gifted
    if kwargs['msg-id'] in ('submysterygift', 'anonsubmysterygift',):
        gift_users = sub_mystery_gift.setdefault(kwargs['room-id'], {})
        gift_users[kwargs['user-id']] = int(kwargs['msg-param-mass-gift-count'])
    if kwargs['msg-id'] in ('subgift', 'anonsubgift'):
        if kwargs['room-id'] in sub_mystery_gift:
            if kwargs['user-id'] in sub_mystery_gift[kwargs['room-id']]:
                sub_mystery_gift[kwargs['room-id']][kwargs['user-id']] -= 1
                if 0 == sub_mystery_gift[kwargs['room-id']][kwargs['user-id']]:
                    del sub_mystery_gift[kwargs['room-id']][kwargs['user-id']]
                else:
                    return

    if kwargs['msg-id'] in ('sub', 'resub', 'subgift', 'anonsubgift', 'giftpaidupgrade',):
        alert = await bot.db.fetchone('SELECT message FROM twitch_chat_alerts WHERE channel_id=%s and type="sub"', (
            kwargs['room-id'],
        ))
        if alert:
            bot.send("PRIVMSG", target=kwargs['channel'], message=alert['message'])
        
        await badge_log( 
            nick=kwargs['login'],
            target=kwargs['channel'],
            **kwargs
        )