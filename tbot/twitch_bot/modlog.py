import asyncio, websockets, random, json, aiohttp
from datetime import datetime, timezone
from tbot import config, utils, logger

class Pubsub():

    def __init__(self):
        self.url = config.data.twitch.pubsub_url
        self.token = config.data.twitch.chat_token
        self.ping_callback = None
        self.pong_check_callback = None
        self.ws = None
        self.loop = asyncio.get_event_loop()

    async def parse_message(self, message):
        if message['type'] == 'PONG':
            logger.debug('Received pong')
            if self.pong_check_callback:
                self.pong_check_callback.cancel()
            self.ping_callback = asyncio.create_task(self.ping())
        elif message['type'] == 'RECONNECT':
            await self.ws.close()
        elif message['type'] == 'MESSAGE':
            m = json.loads(message['data']['message'])
            if message['data']['topic'].startswith('chat_moderator_actions'):
                await self.log_mod_action(message['data']['topic'], m['data'])
            elif message['data']['topic'].startswith('channel-subscribe-events-v1'):
                await self.log_sub(message['data']['topic'], m['data'])

    async def log_mod_action(self, topic, data):
        if 'moderation_action' not in data:
            return
        c = topic.split('.')
        def get_target_user():
            if data.get('target_user_login'):
                return data['target_user_login']
            if data.get('args'):
                return data['args'][0]
        def get_created_by():
            if data.get('created_by'):
                return data['created_by']
            if data.get('created_by_login'):
                return data['created_by_login']
            return 'twitch'
        def created_by_user_id():
            if data.get('created_by_user_id'):
                return data['created_by_user_id']
            if data.get('created_by_id'):
                return data['created_by_id']
            return 0

        try:
            if data['moderation_action'] in ('mod', 'unmod'):
                asyncio.create_task(utils.twitch_save_mods(self, c[2]))

            if data['moderation_action'] == 'delete':
                data['args'] = [data['args'][0], data['args'][-1]]
            self.loop.create_task(self.db.execute('''
                INSERT INTO twitch_modlog (created_at, channel_id, user, user_id, command, args, target_user, target_user_id) VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                datetime.utcnow(),
                c[2],
                get_created_by(),
                created_by_user_id(),
                data['moderation_action'],
                ' '.join(data['args']).strip()[:200] if data.get('args') else '',
                get_target_user(),
                data['target_user_id'] if data.get('target_user_id') else None,
            )))
            if data.get('target_user_id'):
                self.loop.create_task(self.db.execute('''
                    INSERT INTO twitch_chatlog (type, created_at, channel_id, user, user_id, message) VALUES
                        (%s, %s, %s, %s, %s, %s)
                ''', (
                    100,
                    datetime.utcnow(),
                    c[2],
                    get_target_user(),
                    data['target_user_id'],
                    '<{}{} (by {})>'.format(
                        data['moderation_action'],
                        ' '+(' '.join(data['args']).strip() if data.get('args') else '')+
                        ' '+data['moderator_message'] if data.get('moderator_message') else '',
                        get_created_by(),
                    ),
                )))

                if data['moderation_action'] in ['ban', 'timeout', 'delete']:
                    field = data['moderation_action'] + 's'
                    if field == 'timeouts' and data['args'][1] == '1':
                        field = 'purges'
                    r = await self.db.execute('''
                        UPDATE twitch_user_chat_stats SET {0}={0}+1 WHERE channel_id=%s AND user_id=%s
                    '''.format(field), (c[2], data['target_user_id'],))
                    if not r.rowcount:
                        self.loop.create_task(self.db.execute('''
                            INSERT INTO twitch_user_chat_stats (channel_id, user_id, {0}) 
                            VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE {0}={0}+1
                        '''.format(field), (c[2], data['target_user_id'],)))

        except Exception as e:
            logger.exception(e)

    async def log_sub(self, data):
        try:
            user_id = data.get('user_id')
            user = data.get('user_name', 'anonsubgift')
            gifter_id = None
            gifter_user = None
            if data['is_gift']:
                gifter_id = user_id
                gifter_user = user
                user_id = data['recipient_id']
                user = data['recipient_user_name']

            await self.db.execute('''
                INSERT INTO twitch_sub_log (
                    channel_id, 
                    created_at, 
                    user_id, 
                    user,
                    message, 
                    tier, 
                    gifter_id, 
                    gifter,
                    is_gift, 
                    total
                ) VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                data['channel_id'],
                datetime.now(tz=timezone.utc),
                user_id,
                user,
                data['sub_message'].get('message'),
                data['sub_plan'].lower(),
                gifter_id,
                gifter_user,
                data['is_gift'],
                data.get('cumulative_months'),
            ))

            message = data['sub_message'].get('message')
            tiers = {
                '1000': 'Tier 1 Sub',
                '2000': 'Tier 2 Sub',
                '3000': 'Tier 3 Sub',
                'prime': 'Prime Sub',
            }

            if not data['is_gift']:
                if message:
                    message = f': {message}'
                message = f'{user} subscribed with a {tiers.get(data["sub_plan"].lower(), "unknown")} ({data["cumulative_months"]}){message}'
            else:
                message = f'{gifter_user} gifted a {tiers.get(data["sub_plan"].lower(), "unknown")} to {user}'

            await self.db.execute('''
                INSERT INTO twitch_chatlog (type, created_at, channel_id, user, user_id, message) VALUES
                    (%s, %s, %s, %s, %s, %s)
            ''', (
                2,
                datetime.now(tz=timezone.utc),
                data['channel_id'],
                gifter_user or user,
                gifter_id or user_id,
                message,
            ))
        except Exception as e:
            logger.exception(e)

    async def run(self):
        self.ahttp = aiohttp.ClientSession()        
        self.redis_sub = await self.redis.subscribe('tbot:server:commands')
        asyncio.create_task(self.receive_server_commands())

        logger.info('PubSub Connecting to {}'.format(self.url))
        async for ws in websockets.connect(self.url):
            self.ws = ws
            try:
                if self.ping_callback:
                    self.ping_callback.cancel()
                self.ping_callback = asyncio.create_task(self.ping())
                user = await utils.twitch_current_user(self.ahttp)
                logger.info('Connected to PubSub as {}'.format(user['login']))
                self.current_user_id = user['id']
                channels = await self.get_channels() 
                for c in channels:
                    topics = self.get_topics(c['channel_id'], c['twitch_scopes'])
                    if not topics:
                        continue
                    await self.ws.send(json.dumps({
                        'type': 'LISTEN',
                        'nonce': c['channel_id'],
                        'data': {
                            'topics': topics,
                            'auth_token': c['twitch_token'],
                        }
                    }))

                while True:
                    try:
                        data = await self.ws.recv()
                        message = json.loads(data)
                        if message.get('error'):
                            logger.info(message)
                        await self.parse_message(message)
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt()

            except websockets.ConnectionClosed as e:
                self.ping_callback.cancel()
                logger.info(f'Lost connection to {self.url}, reconnecting. {e}')
                continue
            except KeyboardInterrupt:
                raise KeyboardInterrupt()

    async def ping(self):
        await asyncio.sleep(random.randint(200, 300))
        logger.debug('Send PING')
        await self.ws.send('{"type": "PING"}')
        self.pong_check_callback = asyncio.create_task(self.close())

    async def close(self):
        await asyncio.sleep(10)
        logger.info('Closing')
        await self.ws.close()

    async def get_channels(self):
        rows = await self.db.fetchall('''
        SELECT 
            channel_id, name, twitch_scope, twitch_token
        FROM
            twitch_channels
        WHERE
            active="Y";
        ''')
        l = []
        for r in rows:
            l.append({
                'channel_id': r['channel_id'],
                'name': r['name'].lower(),
                'twitch_scopes': utils.json_loads(r['twitch_scope']) if r['twitch_scope'] else [],
                'twitch_token': r['twitch_token'],
            })
        return l

    def get_topics(self, channel_id: str, scopes: list[str]):
        topics = []
        if 'channel:moderate' in scopes:
            topics.append(f'chat_moderator_actions.{channel_id}.{channel_id}')
        if 'channel:read:subscriptions' in scopes:
            topics.append(f'channel-subscribe-events-v1.{channel_id}')
        return topics
        

    async def receive_server_commands(self):
        sub = self.redis_sub[0]
        while (await sub.wait_message()):
            try:
                msg = await sub.get_json()
                logger.debug('Received server command: {}'.format(msg))
                if len(msg) != 2:
                    return
                cmd = msg.pop(0)
                if cmd not in ['join', 'part']:
                    return
                topics = []
                channel = await self.db.fetchone('select twitch_scope, twitch_token from twitch_channels where channel_id=%s', (msg[0],))
                if not channel:
                    return
                scopes = json.loads(channel['twitch_scope']) if channel['twitch_scope'] else []
                topics = self.get_topics(msg[0], scopes)
                type_ = ''
                if cmd == 'join':
                    type_ = 'LISTEN'
                elif cmd == 'part':
                    type_ = 'UNLISTEN'
                await self.ws.send(json.dumps({
                    'type': type_,
                    'data': {
                        'topics': topics,
                        'auth_token': channel['twitch_token'],
                    }
                }))
            except:
                logger.exception('receive_server_commands')