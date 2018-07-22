import asyncio
import sqlalchemy as sa
import logging
from tbot.irc.command import command
from tbot import utils
from datetime import datetime, timedelta

@command('chatstats')
async def chat_stats(client, nick, channel, channel_id, target, args, **kwargs):
    user = kwargs['display-name']
    user_id = kwargs['user-id']
    if len(args) > 0:
        user = utils.safe_username(args[0])
        user_id = await utils.twitch_lookup_user_id(client.http_session, user)

    if not check_channel(client, nick, channel, channel_id, target, args, **kwargs):
        return

    current_stream, current_month = await asyncio.gather(
        current_stream_stats(client, channel_id, user_id),
        user_month_stats(client, channel_id, user_id),
    )

    msg = '{}: {} - {}'.format(
        user,
        current_stream,
        current_month,
    )
    client.send("PRIVMSG", target=target, message=msg)

@command('chatstatslastmonth')
async def chatstatslastmonth(client, nick, channel, channel_id, target, args, **kwargs):
    user = kwargs['display-name']
    user_id = kwargs['user-id']

    if len(args) == 1:
        user = utils.safe_username(args[0])
        user_id = await utils.twitch_lookup_user_id(client.http_session, user)

    last_month = await user_last_month_stats(client, channel_id, user_id)

    msg = '{}: {}'.format(
        user,
        last_month,
    )
    client.send("PRIVMSG", target=target, message=msg)

@command('totalchatstats')
async def total_chat_stats(client, nick, channel, channel_id, target, args, **kwargs):
    if not check_channel(client, nick, channel, channel_id, target, args, **kwargs):
        return

    # get stats for the current stream
    q = await client.conn.execute(sa.sql.text(
        '''SELECT count(message) as msgs, sum(word_count) as words
           FROM logitch.entries WHERE 
           channel_id=:channel_id AND 
           created_at>=:from_date AND 
           type=1;'''),
        {
            'channel_id': channel_id, 
            'from_date': client.channels[channel_id]['went_live_at'],
        }
    )
    r = await q.fetchone()
    if r:
        current_stream = 'This stream: {} messages / {} words'.format(
            r['msgs'], r['words']
        )
    else:
        current_stream = 'This stream: nothing'

    msg = 'Channel chat stats: {}'.format(
        current_stream,
    )
    client.send("PRIVMSG", target=target, message=msg)


async def current_stream_stats(client, channel_id, user_id):
    q = await client.conn.execute(sa.sql.text(
        '''SELECT count(message) as msgs, sum(word_count) as words 
           FROM logitch.entries WHERE 
           channel_id=:channel_id AND 
           user_id=:user_id AND 
           created_at>=:from_date AND 
           type=1
           GROUP BY user_id;'''),
        {
            'channel_id': channel_id, 
            'user_id': user_id,
            'from_date': client.channels[channel_id]['went_live_at'],
        }
    )
    r = await q.fetchone()
    if r:
        return 'This stream: {} messages / {} words'.format(
            r['msgs'], r['words']
        )
    else:
        return 'This stream: nothing'


async def user_month_stats(client, channel_id, user_id):
    from_date = datetime.utcnow().replace(
        day=1, hour=0, minute=0, 
        second=0, microsecond=0,
    )
    q = await client.conn.execute(sa.sql.text(
        '''SELECT count(message) as msgs, sum(word_count) as words 
           FROM logitch.entries WHERE 
           channel_id=:channel_id AND 
           user_id=:user_id AND 
           created_at>=:from_date AND 
           type=1
           GROUP BY user_id;'''),
        {
            'channel_id': channel_id, 
            'user_id': user_id,
            'from_date': from_date,
        }
    )
    r = await q.fetchone()
    if r:
        return 'This month: {} messages / {} words'.format(
            r['msgs'], r['words']
        )
    else:
        return 'This month: nothing'


async def user_last_month_stats(client, channel_id, user_id):
    to_date = datetime.utcnow().replace(
        day=1, hour=0, minute=0, 
        second=0, microsecond=0,
    ) - timedelta(seconds=1)
    from_date = to_date.replace(
        day=1, hour=0, minute=0, 
        second=0, microsecond=0,
    )
    q = await client.conn.execute(sa.sql.text(
        '''SELECT count(message) as msgs, sum(word_count) as words 
           FROM logitch.entries WHERE 
           channel_id=:channel_id AND 
           user_id=:user_id AND 
           created_at>=:from_date AND 
           created_at<=:to_date AND 
           type=1
           GROUP BY user_id;'''),
        {
            'channel_id': channel_id, 
            'user_id': user_id,
            'from_date': from_date,
            'to_date': to_date,
        }
    )
    r = await q.fetchone()
    if r:
        return 'Last month: {} messages / {} words'.format(
            r['msgs'], r['words']
        )
    else:
        return 'Last month: nothing'


def check_channel(client, nick, channel, channel_id, target, args, **kwargs):
    if not client.channels[channel_id]['is_live']:
        msg = '@{}, the stream is offline'.format(kwargs['display-name'])
        client.send("PRIVMSG", target=target, message=msg)
        return

    if not client.channels[channel_id]['went_live_at']:
        msg = '@{}, the stream start time is unknown to me'.format(kwargs['display-name'])
        client.send("PRIVMSG", target=target, message=msg)
        return

    return True