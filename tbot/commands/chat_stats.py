import sqlalchemy as sa
import logging
from tbot.command import command
from tbot import utils
from datetime import datetime

@command('chatstats')
async def chat_stats(client, nick, channel, target, args, **kwargs):
    user = kwargs['display-name']
    user_id = kwargs['user-id']
    if len(args) > 0:
        user = args[0].strip('@')
        user_id = await utils.twitch_lookup_user_id(client.http_session, user)

    if not client.channels[channel]['is_live']:
        msg = '@{}, the stream is offline'.format(kwargs['display-name'])
        client.send("PRIVMSG", target=target, message=msg)
        return

    if not client.channels[channel]['went_live_at']:
        msg = '@{}, the stream start time is unknown to me'.format(kwargs['display-name'])
        client.send("PRIVMSG", target=target, message=msg)
        return

    # get stats for the current stream
    q = await client.conn.execute(sa.sql.text(
        '''SELECT count(message) as msgs, sum(word_count) as words 
           FROM logitch.entries WHERE 
           channel=:channel AND 
           user_id=:user_id AND 
           created_at>=:from_date AND 
           type=1
           GROUP BY user_id;'''),
        {
            'channel': channel, 
            'user_id': user_id,
            'from_date': client.channels[channel]['went_live_at'],
        }
    )
    r = await q.fetchone()
    if r:
        current_stream = 'This stream: {} messages / {} words'.format(
            r['msgs'], r['words']
        )
    else:
        current_stream = 'This stream: nothing'

    # get stats for the current month
    from_date = datetime.utcnow().replace(
        day=1, hour=0, minute=0, 
        second=0, microsecond=0,
    )
    q = await client.conn.execute(sa.sql.text(
        '''SELECT count(message) as msgs, sum(word_count) as words 
           FROM logitch.entries WHERE 
           channel=:channel AND 
           user_id=:user_id AND 
           created_at>=:from_date AND 
           type=1
           GROUP BY user_id;'''),
        {
            'channel': channel, 
            'user_id': user_id,
            'from_date': from_date,
        }
    )
    r = await q.fetchone()
    if r:
        current_month = 'This month: {} messages / {} words'.format(
            r['msgs'], r['words']
        )
    else:
        current_month = 'This month: nothing'

    msg = '{}: {} - {}'.format(
        user,
        current_stream,
        current_month,
    )
    client.send("PRIVMSG", target=target, message=msg)

@command('totalchatstats')
async def total_chat_stats(client, nick, channel, target, args, **kwargs):
    if not client.channels[channel]['is_live']:
        msg = '@{}, the stream is offline'.format(kwargs['display-name'])
        client.send("PRIVMSG", target=target, message=msg)
        return

    if not client.channels[channel]['went_live_at']:
        msg = '@{}, the stream start time is unknown to me'.format(kwargs['display-name'])
        client.send("PRIVMSG", target=target, message=msg)
        return

    # get stats for the current stream
    q = await client.conn.execute(sa.sql.text(
        '''SELECT count(message) as msgs, sum(word_count) as words
           FROM logitch.entries WHERE 
           channel=:channel AND 
           created_at>=:from_date AND 
           type=1;'''),
        {
            'channel': channel, 
            'from_date': client.channels[channel]['went_live_at'],
        }
    )
    r = await q.fetchone()
    if r:
        current_stream = 'This stream: {} messages / {} words'.format(
            r['msgs'], r['words']
        )
    else:
        current_stream = 'This stream: nothing'

    msg = 'Total chat stats: {}'.format(
        current_stream,
    )
    client.send("PRIVMSG", target=target, message=msg)