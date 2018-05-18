import sqlalchemy as sa
from tbot.command import command
from tbot import utils

@command('streamwatchtime', alias='swt')
async def user_stream_watchtime(client, nick, channel, target, args, **kwargs):
    user = kwargs['display-name']
    if len(args) > 0:
        user = args[0].strip('@')

    if not client.channels[channel]['is_live']:
        msg = '@{}, the stream is offline'.format(kwargs['display-name'])
        client.send("PRIVMSG", target=target, message=msg)            
        return

    r = await client.conn.execute(sa.sql.text('SELECT time FROM current_stream_watchtime WHERE channel=:channel AND user=:user'),
        {'channel': channel, 'user': user}
    )
    r = await r.fetchone()

    if not r or (r['time'] == 0):    
        msg = '{} is unknown to me'.format(user)
        client.send("PRIVMSG", target=target, message=msg)
        return

    total_live_seconds = (client.channels[channel]['last_check'].replace(second=0, microsecond=0) - \
        client.channels[channel]['went_live_at'].replace(second=0)).total_seconds()
    p = r['time'] / total_live_seconds
    msg = '{} has been here for {} this stream ({:.0%})'.format(
        user, 
        utils.seconds_to_pretty(r['time']),
        p
    )
    client.send("PRIVMSG", target=target, message=msg)
