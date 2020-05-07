import asyncio, websockets, logging, random, json, aioredis, aiohttp
from datetime import datetime
from tbot import config, db, utils

class Pubsub():

    def __init__(self):
        self.url = config['twitch']['pubsub_url']
        self.token = config['twitch']['chat_token']
        self.ping_callback = None
        self.pong_check_callback = None
        self.ws = None
        self.loop = asyncio.get_event_loop()

    async def parse_message(self, message):
        if message['type'] == 'PONG':
            asyncio.ensure_future(self.ping())
            if self.pong_check_callback:
                self.pong_check_callback.cancel()
        elif message['type'] == 'RECONNECT':
            await self.ws.close()
        elif message['type'] == 'MESSAGE':
            m = json.loads(message['data']['message'])
            self.loop.create_task(self.log_mod_action(message['data']['topic'], m['data']))

    async def log_mod_action(self, topic, data):
        if 'moderation_action' not in data:
            return
        c = topic.split('.')
        try:
            if data['moderation_action'] == 'delete':
                data['args'] = [data['args'][0], data['args'][-1]]
            self.loop.create_task(self.db.execute('''
                INSERT INTO twitch_modlog (created_at, channel_id, user, user_id, command, args, target_user, target_user_id) VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                datetime.utcnow(),
                c[2],
                data['created_by'] or 'twitch',
                data['created_by_user_id'] or 0,
                data['moderation_action'],
                ' '.join(data['args']).strip()[:200] if data['args'] else '',
                data['args'][0] if data['target_user_id'] else None,
                data['target_user_id'] if data['target_user_id'] else None,
            )))
            if data['target_user_id']:
                self.loop.create_task(self.db.execute('''
                    INSERT INTO twitch_chatlog (type, created_at, channel_id, user, user_id, message) VALUES
                        (%s, %s, %s, %s, %s, %s)
                ''', (
                    100,
                    datetime.utcnow(),
                    c[2],
                    data['args'][0],
                    data['target_user_id'],
                    '<{}{} (by {})>'.format(
                        data['moderation_action'],
                        ' '+' '.join(data['args']).strip() if data['args'] else '',
                        data['created_by'] or 'twitch',
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
            logging.exception('log_mod_action')

    async def run(self):
        self.db = await db.Db().connect(self.loop)
        self.ahttp = aiohttp.ClientSession()     
        self.redis = await aioredis.create_redis_pool(
            'redis://{}:{}'.format(config['redis']['host'], config['redis']['port']),
            minsize=config['redis']['pool_min_size'], 
            maxsize=config['redis']['pool_max_size'],
            loop=self.loop,
        )
        self.redis_sub = await self.redis.subscribe('tbot:server:commands')
        asyncio.ensure_future(self.receive_server_commands())
        while True:
            if self.ws:
                self.ws.close()
            try:
                await self.connect()
                while True:
                    try:
                        message = await self.ws.recv()
                        await self.parse_message(json.loads(message))
                    except websockets.exceptions.ConnectionClosed as e:
                        self.ping_callback.cancel()
                        logging.error(f'PubSub connection closed: {e.reason}')
                        break
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt()
                    except:
                        logging.exception('Loop 2')
            except KeyboardInterrupt:
                break
            except:
                logging.exception('Loop 1')
                await asyncio.sleep(10)

    async def connect(self):
        if self.ping_callback:
            self.ping_callback.cancel()
        user = await utils.twitch_current_user(self.ahttp)
        self.current_user_id = user['id']
        channels = await self.get_channels() 
        topics = []
        for c in channels:
            topics.append('chat_moderator_actions.{}.{}'.format(
                self.current_user_id,
                c['channel_id'],
            ))
        logging.info('PubSub Connecting to {}'.format(self.url))
        self.ws = await websockets.connect(self.url)
        await self.ws.send(json.dumps({
            'type': 'LISTEN',
            'data': {
                'topics': topics,
                'auth_token': self.token,
            }
        }))
        self.ping_callback = asyncio.ensure_future(self.ping())

    async def ping(self):
        await asyncio.sleep(random.randint(120, 240))
        await self.ws.send('{"type": "PING"}')
        self.pong_check_callback = asyncio.ensure_future(self.close())

    async def close(self):
        await asyncio.sleep(10)
        logging.info('closing')
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
                logging.debug('Received server command: {}'.format(msg))
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
                logging.exception('receive_server_commands')

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load('../../tbot.yaml')    
    logger.set_logger('modlog.log')
    loop = asyncio.get_event_loop()
    loop.create_task(Pubsub().run())    
    loop.run_forever()