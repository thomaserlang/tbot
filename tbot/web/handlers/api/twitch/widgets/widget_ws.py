import asyncio, logging
from tornado import websocket
from tbot import utils

connections = {}
sub_messages_running = False
listeners = {}

class Handler(websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info = None
        self.redis_sub = None

    def open(self):
        pass

    async def on_message(self, message):
        try:
            message = utils.json_loads(message)
            typ = message.get('type')
            if typ == 'PING':
                await self.write_message({'type': 'PONG'})
            elif typ == 'LISTEN':
                await self.get_widget(message['data'].get('key'))
            else:
                await self.write_message({'type': 'ERROR', 'message': f'Unknown type: {typ}'})
        except ValueError as e:
            await self.write_message({'type': 'ERROR', 'message': 'Invalid body, just be JSON'})

    def on_close(self):
        if self in connections:
            for key in connections[self]:
                listeners[key].remove(self)
            del connections[self]

    async def get_widget(self, key):
        r = await self.db.fetchone(
            'SELECT channel_id, type, settings FROM twitch_widget_keys WHERE `key`=%s', 
            (key,)
        )
        if not r:
            await self.write_message({'type': 'ERROR', 'message': 'Invalid widget key'})
            return
        r['settings'] = utils.json_loads(r['settings']) if r['settings'] else {}
        self.info = r
        await self.sub(f'twitch:widget:goal:{self.info["channel_id"]}:{self.info["settings"]["type"]}')
        await self.write_message(r)
    
    async def sub(self, key):
        global sub_messages_running
        if not sub_messages_running:
            asyncio.create_task(sub_messages(self.redis))
        l = listeners.setdefault(key, [])
        l.append(self)
        c = connections.setdefault(self, [])
        c.append(key)

    async def unsub(self):
        return

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    @property
    def ahttp(self):
        return self.application.ahttp

async def sub_messages(redis):
    global sub_messages_running
    sub_messages_running = True
    redis_sub, = await redis.psubscribe(f'twitch:widget:*')
    while await redis_sub.wait_message():
        channel, data = await redis_sub.get()
        name = channel.decode('utf-8')
        if name in listeners:
            for s in listeners[name]:
                await s.write_message(data)