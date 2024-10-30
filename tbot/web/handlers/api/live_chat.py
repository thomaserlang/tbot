from tornado import ioloop, websocket

from tbot import logger


class LiveChatHandler(websocket.WebSocketHandler):
    clients_by_channel = {}
    clients_to_channels = {}
    redis_channels = {}

    async def open(self, channel_id: str):
        if channel_id not in LiveChatHandler.clients_by_channel:
            LiveChatHandler.clients_by_channel[channel_id] = set()
        LiveChatHandler.clients_by_channel[channel_id].add(self)

        if self not in LiveChatHandler.clients_to_channels:
            LiveChatHandler.clients_to_channels[self] = set()
        LiveChatHandler.clients_to_channels[self].add(channel_id)

        if channel_id not in LiveChatHandler.redis_channels:
            ioloop.IOLoop.current().add_callback(self.listen_to_redis, channel_id)

    async def listen_to_redis(self, channel_id: str):
        while True:
            try:
                LiveChatHandler.redis_channels[
                    channel_id
                ] = await self.application.redis.subscribe(
                    f'tbot:live_chat:{channel_id}'
                )
                sub = LiveChatHandler.redis_channels[channel_id][0]
                while await sub.wait_message():
                    try:
                        message = await sub.get()
                        for client in LiveChatHandler.clients_by_channel.get(
                            channel_id, set()
                        ):
                            client.write_message(message.decode('utf-8'))
                    except websocket.WebSocketClosedError:
                        self.on_close()
                    except Exception as e:
                        logger.exception(e)
            except Exception as e:
                logger.exception(e)

    async def on_message(self, message):
        pass

    def on_close(self):
        async def close():
            for channel_id in LiveChatHandler.clients_to_channels.get(self, set()):
                if channel_id in LiveChatHandler.clients_by_channel:
                    LiveChatHandler.clients_by_channel[channel_id].remove(self)
                    if not LiveChatHandler.clients_by_channel[channel_id]:
                        await self.application.redis.unsubscribe(
                            f'tbot:live_chat:{channel_id}'
                        )
                        del LiveChatHandler.clients_by_channel[channel_id]
                        del LiveChatHandler.redis_channels[channel_id]

            if self in LiveChatHandler.clients_to_channels:
                del LiveChatHandler.clients_to_channels[self]

        ioloop.IOLoop.current().add_callback(close)
