import logging
import sqlalchemy as sa
from datetime import datetime
from tbot.command import command
from tbot import utils

@command('streamwatchtime', alias='swt')
async def user_stream_watchtime(client, nick, channel, target, args, **kwargs):
    user = kwargs['display-name']
    user_id = kwargs['user-id']
    if len(args) > 0:
        user = utils.safe_username(args[0])
        user_id = await utils.twitch_lookup_user_id(client.http_session, user)

    if not client.channels[channel]['is_live']:
        msg = '@{}, the stream is offline'.format(kwargs['display-name'])
        client.send("PRIVMSG", target=target, message=msg)            
        return

    r = await client.conn.execute(sa.sql.text(
        'SELECT time FROM stream_watchtime WHERE channel=:channel AND stream_id=:stream_id AND user_id=:user_id'),
        {
            'channel': channel, 
            'stream_id': client.channels[channel]['stream_id'], 
            'user_id': user_id,
        }
    )
    r = await r.fetchone()

    if not r or (r['time'] == 0):    
        msg = '{} is unknown to me'.format(user)
        client.send("PRIVMSG", target=target, message=msg)
        return

    total_live_seconds = round((client.channels[channel]['last_check'] - \
        client.channels[channel]['went_live_at']).total_seconds())
    usertime = r['time']
    
    if (usertime > total_live_seconds) or ((total_live_seconds - usertime) <= 60):
        usertime = total_live_seconds

    p = usertime / total_live_seconds
    msg = '{} has been here for {} this stream ({:.0%})'.format(
        user, 
        utils.seconds_to_pretty(usertime),
        p
    )
    client.send("PRIVMSG", target=target, message=msg)
