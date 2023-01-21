import asyncio, websockets, random, json, aiohttp
from datetime import datetime
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
            self.loop.create_task(self.log_mod_action(message['data']['topic'], m['data']))

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

        except:
            logger.exception('log_mod_action')

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
                self.current_user_id = user['id']
                channels = await self.get_channels() 
                topics = []
                for c in channels:
                    topics.append('chat_moderator_actions.{}.{}'.format(
                        self.current_user_id,
                        c['channel_id'],
                    ))
                if topics:
                    await self.ws.send(json.dumps({
                        'type': 'LISTEN',
                        'data': {
                            'topics': topics,
                            'auth_token': self.token,
                        }
                    }))

                while True:
                    try:
                        message = await self.ws.recv()
                        await self.parse_message(json.loads(message))
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
            channel_id, name
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
            })
        return l

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
                topic = 'chat_moderator_actions.{}.{}'.format(
                    self.current_user_id,
                    msg[0],
                )
                type_ = ''
                if cmd == 'join':
                    type_ = 'LISTEN'
                elif cmd == 'part':
                    type_ = 'UNLISTEN'
                await self.ws.send(json.dumps({
                    'type': type_,
                    'data': {
                        'topics': [topic],
                        'auth_token': self.token,
                    }
                }))
            except:
                logger.exception('receive_server_commands')