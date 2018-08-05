import logging
from tbot import config, utils
from tbot.twitch_bot import bot

@bot.on('USERNOTICE')
async def usernotice(**kwargs):
    if kwargs['msg-id'] in ('sub', 'resub', 'subgift'):
        '''
        {'channel': '#shroud', 'message': None, 'badges': 'subscriber/3,premium/1', 'color': '#1E90FF', 'display-name': 'Ai0li', 'emotes': '', 'id': '42e1c41f-23f5-4b9c-93f9-c7b7278400ff', 'login': 'ai0li', 'mod': '0', 'msg-id': 'resub', 'msg-param-months': '4', 'msg-param-sub-plan-name': 'Channel Subscription (meclipse)', 'msg-param-sub-plan': 'Prime', 'room-id': '37402112', 'subscriber': '1', 'system-msg': 'Ai0li just subscribed with Twitch Prime. Ai0li subscribed for 4 months in a row!', 'tmi-sent-ts': '1533233279635', 'turbo': '0', 'user-id': '44003032', 'user-type': ''}
        '''
        alert = await bot.db.fetchone('SELECT message FROM chat_alerts WHERE channel_id=%s and type="sub"', (
            kwargs['room-id'],
        ))
        if not alert:
            return
        bot.send("PRIVMSG", target=kwargs['channel'], message=alert['message'])