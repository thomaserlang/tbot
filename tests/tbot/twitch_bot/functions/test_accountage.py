import unittest, nose, asyncio
from functools import partial
from unittest import mock
from tbot.twitch_bot import functions
from datetime import datetime

async def mock_result(*args, **kwargs):
    return {
        "_id": "44322889",
        "bio": "Just a gamer playing games and chatting. :)",
        "created_at": "2013-06-03T19:12:02.580593Z",
        "display_name": "dallas",
        "logo": "https://static-cdn.jtvnw.net/jtv_user_pictures/dallas-profile_image-1a2c906ee2c35f12-300x300.png",
        "name": "dallas",
        "type": "staff",
        "updated_at": "2016-12-13T16:31:55.958584Z"
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
            'accountage': '5 years, 8 months, 13 days and 2 hours',
            'accountage_date': '2013-06-03',
            'accountage_datetime': '2013-06-03 19:12:02 UTC',
        })


if __name__ == '__main__':
    nose.run(defaultTest=__name__)