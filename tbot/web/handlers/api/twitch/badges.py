from tbot.utils.twitch import twitch_request
from tbot.web.handlers.api.base import Api_handler


class BadgesHandler(Api_handler):
    async def get(self, channel_id):
        badges = await twitch_request(
            self.ahttp, url='https://api.twitch.tv/helix/chat/badges/global'
        )
        channel_badges = await twitch_request(
            self.ahttp,
            url=f'https://api.twitch.tv/helix/chat/badges?broadcaster_id={channel_id}',
        )
        self.write_object(
            {
                'global_badges': badges['data'],
                'channel_badges': channel_badges['data'],
            }
        )
