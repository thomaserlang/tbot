import good
from ..base import Api_handler, Level, Api_exception

from tbot.utils.twitch import twitch_channel_token_request, Twitch_request_error

class Handler(Api_handler):
    
    __schema__ = good.Schema({
        'length': good.Coerce(int),
    })

    @Level(3)
    async def post(self, channel_id):
        data = self.validate()
        try:
            data = await twitch_channel_token_request(
                self, 
                channel_id=channel_id,
                url='https://api.twitch.tv/helix/channels/commercial',
                method='POST',
                json={
                    'broadcaster_id': channel_id,
                    'length': data['length'],
                }
            )
            self.write({
                'retry_after': data['data'][0]['retry_after'],
                'message': data['data'][0]['message'],
            })
        except Twitch_request_error as e:
            raise Api_exception(e.status_code, e.message, e.extra)