from tbot.utils.twitch import twitch_request
from tbot.web.handlers.api.base import Api_handler


class EmotesHandler(Api_handler):
    async def get(self, channel_id):
        emotes = await twitch_request(
            self.ahttp, url='https://api.twitch.tv/helix/chat/emotes/global'
        )
        channel_emotes = await twitch_request(
            self.ahttp,
            url=f'https://api.twitch.tv/helix/chat/emotes?broadcaster_id={channel_id}',
        )
        self.write_object(
            {
                'global_emotes': emotes['data'],
                'channel_emotes': channel_emotes['data'],
            }
        )
