import unittest, nose, asyncio
from functools import partial
from unittest import mock
from tbot.twitch_bot import functions
from datetime import datetime

async def mock_result(*args, **kwargs):
    return {
        "total": 1,
        "data": [
            {
                "from_id": "1",
                "from_name": "Test1",
                "to_id": "2",
                "to_name": "Test2",
                "followed_at": "2018-02-15T13:44:37Z"
            }
        ],
        "pagination": {}
    }

class Test(unittest.TestCase):

    @mock.patch('tbot.utils.twitch_request', side_effect=mock_result)
    @mock.patch('tbot.twitch_bot.functions.followage.datetime')
    def test(self, dt, twitch_request):
        dt.utcnow.return_value = datetime(2019, 1, 16, 21, 36, 55)
        bot = mock.MagicMock()
        bot.ahttp = None
        loop = asyncio.get_event_loop()
        s = loop.run_until_complete(loop.create_task(
            functions.followage.followage(
                bot=bot,
                user_id='1',
                display_name='Test1', 
                channel_id='2',
                channel='test2',
                args=[],
            )
        ))
        self.assertEqual(s, {
            'followage': '11 months, 5 days and 7 hours',
            'followage_date': '2018-02-15',
            'followage_datetime': '2018-02-15 13:44:37 UTC',
        })


if __name__ == '__main__':
    nose.run(defaultTest=__name__)