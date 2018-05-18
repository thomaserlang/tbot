from tbot.command import command
from tbot import utils

@command('streamwatchtime', alias='swt')
async def user_stream_watchtime(client, nick, channel, target, args, **kwargs):
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

    total_live_seconds = round((client.channels[channel]['last_check'] - \
        client.channels[channel]['went_live_at']).total_seconds())
    p = r['time'] / total_live_seconds
    msg = '{} has been here for {} this stream ({:.0%})'.format(
        user, 
        utils.seconds_to_pretty(r['time']),
        p
    )
    client.send("PRIVMSG", target=target, message=msg)
