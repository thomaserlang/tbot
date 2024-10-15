import asyncio

from httpx import AsyncClient

from tbot import config, logger
from tbot.twitch_bot.bot_base import bot
from tbot.twitch_bot.tasks.channels_check import cache_channel
from tbot.twitch_bot.tasks.command import db_command

client = AsyncClient()

_started = False


@bot.on('AFTER_CONNECTED')
async def connected(**kwargs):
    global _started
    if not config.data.youtube.client_id:
        return
    if not _started:
        _started = True
        bot.loop.create_task(runner())


async def runner():
    while True:
        await asyncio.sleep(1)
        bot.loop.create_task(check_youtubes_chat())


async def check_youtubes_chat():
    channels = await bot.db.fetchall(
        'SELECT c.channel_id FROM twitch_channels c, twitch_youtube y WHERE c.active=1 AND c.channel_id=y.channel_id',
    )
    for t in channels:
        bot.loop.create_task(check_youtube_chat(t['channel_id']))


async def check_youtube_chat(channel_id: str):
    live_chat_id = await get_live_chat_id(channel_id)
    logger.debug(f'Checking youtube chat for {channel_id} ({live_chat_id})')

    if not live_chat_id:
        return

    chat = await get_youtube_chat(channel_id, live_chat_id)
    if chat.get('offlineAt'):
        bot.channels_check[channel_id]['youtube_live_chat_id'] = None
        await cache_channel(channel_id)
        return

    for m in chat.get('items', []):
        if m['snippet']['type'] != 'textMessageEvent':
            continue
        message = m['snippet']['displayMessage']
        logger.debug(f'Received message {message}')
        author = m['snippet']['authorChannelId']
        author_name = m['authorDetails']['displayName']
        if not message.startswith('!'):
            continue
        if author_name == bot.user['login']:
            continue
        args = message.split(' ')
        cmd = args.pop(0).lower().strip('!')

        badges = ''
        if m['authorDetails']['isChatModerator']:
            badges += 'moderator,'
        if m['authorDetails']['isChatOwner']:
            badges += 'broadcaster,'

        send_msg = await db_command(
            cmd=cmd,
            data={
                'bot': bot,
                'args': args,
                'user': author_name,
                'display_name': author_name,
                'user_id': author,
                'channel': bot.channels[channel_id]['name'],
                'channel_id': channel_id,
                'badges': badges,
                'emotes': '',
                'cmd': cmd,
            },
        )
        if send_msg:
            logger.debug(
                f'Matched command: {cmd} - Sending to YouTube chat: {send_msg} ({live_chat_id})'
            )
            await send_youtube_chat(
                config.data.youtube.twitch_bot_channel_id or channel_id,
                live_chat_id,
                send_msg,
            )


async def send_youtube_chat(channel_id: str, live_chat_id: str, message: str):
    await youtube_request(
        channel_id,
        url='https://www.googleapis.com/youtube/v3/liveChat/messages',
        method='POST',
        params={
            'part': 'snippet',
        },
        json={
            'snippet': {
                'liveChatId': live_chat_id,
                'type': 'textMessageEvent',
                'textMessageDetails': {
                    'messageText': message,
                },
            },
        },
    )


async def get_youtube_chat(channel_id: str, live_chat_id: str):
    chat = await youtube_request(
        channel_id,
        url='https://www.googleapis.com/youtube/v3/liveChat/messages',
        params={
            'part': 'snippet,authorDetails',
            'liveChatId': live_chat_id,
            'pageToken': bot.channels_check[channel_id]['youtube_chat_next_page_token'],
        },
    )
    bot.channels_check[channel_id]['youtube_chat_next_page_token'] = chat.get(
        'nextPageToken', ''
    )
    await cache_channel(channel_id)
    return chat


async def youtube_request(
    channel_id: str, url, params={}, headers={}, method='GET', data=None, json=None
):
    yt = await bot.db.fetchone(
        'select token, refresh_token from twitch_youtube where channel_id=%s',
        (channel_id,),
    )
    if not yt or not yt['token']:
        raise Exception('No youtube account connected')

    headers.update(
        {
            'Authorization': f'Bearer {yt["token"]}',
        }
    )

    r = await client.request(
        method,
        url,
        params=params,
        headers=headers,
        data=data,
        json=json,
    )
    if r.status_code == 401:
        r = await client.post(
            'https://oauth2.googleapis.com/token',
            params={
                'client_id': config.data.youtube.client_id,
                'client_secret': config.data.youtube.client_secret,
                'refresh_token': yt['refresh_token'],
                'grant_type': 'refresh_token',
            },
        )
        if r.status_code != 200:
            raise Exception('Failed to refresh token')
        yt = r.json()

        await bot.db.execute(
            'update twitch_youtube set token=%s where channel_id=%s',
            (yt['access_token'], channel_id),
        )
        headers['Authorization'] = f'Bearer {yt["access_token"]}'

        r = await client.request(
            method,
            url,
            params=params,
            headers=headers,
            data=data,
            json=json,
        )
    try:
        r.raise_for_status()
    except Exception as e:
        logger.error(f'Youtube request failed: {r.text}')
        raise e
    return r.json()


async def get_live_chat_id(channel_id: str):
    if bot.channels_check[channel_id].get('youtube_live_chat_id'):
        return bot.channels_check[channel_id]['youtube_live_chat_id']

    live = await youtube_request(
        channel_id,
        'https://www.googleapis.com/youtube/v3/liveBroadcasts',
        params={
            'part': 'snippet',
            'mine': 'true',
        },
    )
    if not live or not live['items']:
        logger.debug(f'No live broadcast for {channel_id}')
        return

    logger.debug(
        f'Got live broadcast for {channel_id} - {live["items"][0]["snippet"]["liveChatId"]}'
    )

    live_chat_id = live['items'][0]['snippet']['liveChatId']
    bot.channels_check[channel_id]['youtube_live_chat_id'] = live_chat_id
    await cache_channel(channel_id)
    return live_chat_id
