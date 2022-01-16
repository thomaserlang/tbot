import unittest, asyncio
import tbot.testbase
from functools import partial
from unittest import mock
from tbot.twitch_bot import functions
from datetime import datetime

async def mock_result(*args, **kwargs):
    return {
        "data": [
            {
            "id": "141981764",
            "login": "twitchdev",
            "display_name": "TwitchDev",
            "type": "",
            "broadcaster_type": "partner",
            "description": "Supporting third-party developers building Twitch integrations from chatbots to game integrations.",
            "profile_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png",
            "offline_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/3f13ab61-ec78-4fe6-8481-8682cb3b0ac2-channel_offline_image-1920x1080.png",
            "view_count": 5980557,
            "email": "not-real@email.com",
            "created_at": "2016-12-14T20:32:28Z"
            }
        ]
    }

class Test(unittest.TestCase):

    @mock.patch('tbot.utils.twitch_request', side_effect=mock_result)
    @mock.patch('tbot.twitch_bot.functions.accountage.datetime')
    def test(self, dt, twitch_request):
        dt.utcnow.return_value = datetime(2019, 1, 16, 21, 36, 55)
        bot = mock.MagicMock()
        bot.ahttp = None
        loop = asyncio.get_event_loop()
        s = loop.run_until_complete(loop.create_task(
            functions.accountage.accountage(
                bot=bot,
                user_id='44322889',
                display_name='dallas',
                args=[],
            )
        ))
        self.assertEqual(s, {
            'accountage': '2 years, 1 month and 2 days',
            'accountage_date': '2016-12-14',
            'accountage_datetime': '2016-12-14 20:32:28 UTC',
        })


if __name__ == '__main__':
    tbot.testbase.run_file(__file__)