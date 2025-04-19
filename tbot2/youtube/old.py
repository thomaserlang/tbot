import asyncio
from datetime import UTC, datetime
from uuid import uuid4

import httpx
from dateutil.parser import parse as parse_dt
from httpx import AsyncClient
from tbot import config, logger
from tbot.twitch_bot.bot_base import bot
from tbot.twitch_bot.tasks.channels_check import cache_channel
from tbot.twitch_bot.tasks.command import db_command

client = AsyncClient()

_started = False

channel_tasks: dict[str, asyncio.Task] = {}

youtube_bot_channel_id: str = ''


@bot.on('AFTER_CHANNELS_JOINED')
async def connected(**kwargs):
    global _started
    global youtube_bot_channel_id
    if not config.data.youtube.client_id:
        return
    if not _started:
        _started = True
        logger.info('Starting youtube chat tasks')
        youtube_bot_channel_id = await get_bot_channel_id() or ''
        await asyncio.sleep(5)
        await create_tasks()


@bot.on('REDIS_SERVER_COMMAND')
async def redis_server_command(cmd, cmd_args):
    if cmd in ('youtube_connected', 'join'):
        logger.debug(f'Starting youtube chat task for {cmd_args[0]}')
        if not channel_tasks.get(cmd_args[0]):
            channel_tasks[cmd_args[0]] = bot.loop.create_task(
                check_youtube_chat(cmd_args[0])
            )

    if cmd in ('youtube_disconnected', 'part'):
        logger.debug(f'Canceling youtube chat task for {cmd_args[0]}')
        if channel_tasks.get(cmd_args[0]):
            channel_tasks[cmd_args[0]].cancel()
            del channel_tasks[cmd_args[0]]
            bot.channels_check[cmd_args[0]]['youtube_live_chat_id'] = None
            await cache_channel(cmd_args[0])


async def create_tasks():
    logger.info('Setting up youtube chat tasks')
    channels = await bot.db.fetchall(
        'SELECT c.channel_id FROM twitch_channels c, twitch_youtube y WHERE c.active=1 AND c.channel_id=y.channel_id',
    )
    for t in channels:
        logger.debug(f'Starting youtube chat task for {t["channel_id"]}')
        channel_tasks[t['channel_id']] = bot.loop.create_task(
            check_youtube_chat(t['channel_id'])
        )


async def check_youtube_chat(channel_id: str):
    while True:
        try:
            live_chat_id = await get_live_chat_id(channel_id)
            if not live_chat_id:
                await asyncio.sleep(60)
                continue

            chat = await get_youtube_chat(channel_id, live_chat_id)
            if chat.get('offlineAt'):
                bot.channels_check[channel_id]['youtube_live_chat_id'] = None
                await cache_channel(channel_id)
                await asyncio.sleep(60)
                continue

            _ = asyncio.create_task(parse_snippit(channel_id, live_chat_id, chat))

            await asyncio.sleep(chat['pollingIntervalMillis'] / 1000)
        except httpx.HTTPStatusError as e:
            if 'liveStreamingNotEnabled' in e.response.text:
                logger.info(
                    f'Live streaming not enabled for {channel_id}, removing youtube chat task'
                )
                channel_tasks[channel_id].cancel()
                del channel_tasks[channel_id]
                bot.channels_check[channel_id]['youtube_live_chat_id'] = None
                await cache_channel(channel_id)
            elif 'liveChatEnded' in e.response.text:
                bot.channels_check[channel_id]['youtube_live_chat_id'] = None
                await cache_channel(channel_id)
                await asyncio.sleep(60)
            elif 'liveChatNotFound' in e.response.text:
                await asyncio.sleep(60)
            else:
                logger.exception(e)
                await asyncio.sleep(60)
        except Exception as e:
            logger.exception(e)
            await asyncio.sleep(60)


async def parse_snippit(channel_id: str, live_chat_id: str, chat: dict):
    for m in chat.get('items', []):
        if (
            datetime.now(tz=UTC) - parse_dt(m['snippet']['publishedAt'])
        ).total_seconds() > 30:
            continue
        type: str = m['snippet']['type']
        if type == 'textMessageEvent':
            await parse_chatmessages(channel_id, live_chat_id, m)
        elif type in (
            'messageDeletedEvent',
            'userBannedEvent',
        ):
            await parse_mod_action(channel_id, live_chat_id, m)
        elif type in (
            'newSponsorEvent',
            'memberMilestoneChatEvent',
            'superChatEvent',
            'superStickerEvent',
            'membershipGiftingEvent',
            'giftMembershipReceivedEvent',
        ):
            await bot.redis.publish_json(
                f'tbot:live_chat:{channel_id}',
                {
                    'type': 'notice',
                    'provider': 'youtube',
                    'subtype': type,
                    'message': m['snippet'].get('displayMessage', ''),
                    'created_at': m['snippet']['publishedAt'],
                    'user_color': '',
                    'id': str(uuid4()),
                    'data': m['id'],
                },
            )


async def parse_chatmessages(channel_id: str, live_chat_id: str, data: dict):
    await bot.redis.publish_json(
        f'tbot:live_chat:{channel_id}',
        {
            'type': 'message',
            'provider': 'youtube',
            'user_id': data['snippet']['authorChannelId'],
            'user': data['authorDetails']['displayName'],
            'message': data['snippet']['displayMessage'],
            'created_at': data['snippet']['publishedAt'],
            'user_color': '',
            'id': str(uuid4()),
        },
    )

    message = data['snippet']['displayMessage']
    author = data['snippet']['authorChannelId']
    author_name = data['authorDetails']['displayName']
    logger.debug(f'     RECEIVIED: {author_name} - {message}')
    if not message.startswith('!'):
        return
    if author_name == bot.user['login']:
        return
    args = message.split(' ')
    cmd = args.pop(0).lower().strip('!')

    badges = ''
    if data['authorDetails']['isChatModerator']:
        badges += 'moderator,'
    if data['authorDetails']['isChatOwner']:
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
            f'      Matched command: {cmd} - Sending to YouTube chat: {send_msg} ({live_chat_id})'
        )
        await send_youtube_chat(
            config.data.youtube.twitch_bot_channel_id or channel_id,
            live_chat_id,
            send_msg,
        )


async def parse_mod_action(channel_id: str, live_chat_id: str, data: dict):
    message = ''
    mod_user = data['authorDetails']['displayName']
    if data['snippet']['type'] == 'messageDeletedEvent':
        user = data['snippet']['messageDeletedDetails']['displayName']
        message = f'{mod_user} deleted {user}'
    elif data['snippet']['type'] == 'userBannedEvent':
        user = data['snippet']['userBannedDetails']['bannedUserDetails']['displayName']
        if data['snippet']['userBannedDetails']['banType'] == 'permanent':
            message = f'{mod_user} banned {user}'
        else:
            duration = data['snippet']['userBannedDetails']['banDurationSeconds']
            message = f'{mod_user} timed out {user} for {duration} seconds'

    await bot.redis.publish_json(
        f'tbot:live_chat:{channel_id}',
        {
            'type': 'mod_action',
            'provider': 'youtube',
            'subtype': data['snippet']['type'],
            'message': message,
            'created_at': data['snippet']['publishedAt'],
            'user_color': '',
            'id': data['id'],
            'data': data,
        },
    )


async def send_youtube_chat(sender_channel_id: str, live_chat_id: str, message: str):
    await youtube_request(
        sender_channel_id,
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
        logger.error(f'Youtube request failed for channel {channel_id}: {r.text}')
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
    await add_moderator(channel_id, youtube_bot_channel_id, live_chat_id)
    return live_chat_id


async def add_moderator(channel_id: str, moderator_id: str, live_chat_id: str):
    await youtube_request(
        channel_id,
        'https://www.googleapis.com/youtube/v3/liveChat/moderators',
        method='POST',
        params={
            'part': 'snippet',
        },
        json={
            'snippet': {
                'liveChatId': live_chat_id,
                'moderatorDetails': {
                    'channelId': moderator_id,
                },
            },
        },
    )


async def get_bot_channel_id() -> str | None:
    if not config.data.youtube.twitch_bot_channel_id:
        return
    if not config.data.youtube.client_id:
        return
    r = await youtube_request(
        config.data.youtube.twitch_bot_channel_id,
        'https://www.googleapis.com/youtube/v3/channels',
        params={
            'part': 'snippet',
            'mine': 'true',
        },
    )
    return r['items'][0]['id']