import unittest, asyncio
import tbot.testbase
from functools import partial
from unittest import mock
from tbot.twitch_bot import functions
from datetime import datetime

async def mock_result(*args, **kwargs):
    return {
        "total": 12345,
        "data": [
            {
                "from_id": "171003792",
                "from_login": "iiisutha067iii",
                "from_name": "IIIsutha067III",
                "to_id": "23161357",
                "to_name": "LIRIK",
                "followed_at": "2017-08-22T22:55:24Z"
            },
            {
                "from_id": "113627897",
                "from_login": "birdman616",
                "from_name": "Birdman616",
                "to_id": "23161357",
                "to_name": "LIRIK",
                "followed_at": "2017-08-22T22:55:04Z"
            },
        ],
        "pagination":{
            "cursor": "eyJiIjpudWxsLCJhIjoiMTUwMzQ0MTc3NjQyNDQyMjAwMCJ9"
        }
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
            'followage': '1 year, 4 months and 24 days',
            'followage_date': '2017-08-22',
            'followage_datetime': '2017-08-22 22:55:24 UTC',
        })


if __name__ == '__main__':
    tbot.testbase.run_file(__file__)