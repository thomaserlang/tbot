import unittest, nose, asyncio
from unittest.mock import MagicMock
from tbot.twitch_bot.var_filler import parse, format_response, fill_message, var_fillers
from tbot.twitch_bot import functions

class Test_parser(unittest.TestCase):

    def test(self):
        s = 'Viewers: {viewers} Test: {triGgeR test1 test2}'
        r = parse(s)
        self.assertEqual(r[0]['var'], 'viewers')
        self.assertEqual(r[1]['var'], 'triGgeR')
        self.assertEqual(r[1]['args'], ['test1', 'test2'])

        r[0]['value'] = '100'
        r[1]['value'] = 'Erle'
        self.assertEqual(format_response(s, r), 'Viewers: 100 Test: Erle')

class Test_filler(unittest.TestCase):

    def test(self):
        bot = MagicMock()
        bot.db.fetchone = mock_result

        loop = asyncio.get_event_loop()
        m = 'Chat stats: {user.chat_stats.stream_msgs} ({user.chat_stats.stream_words})'
        s = loop.run_until_complete(fill_message(m, bot=bot, channel_id=1, args=[], user_id=123))
        self.assertEqual(s, 'Chat stats: 3 messages (5 words)')

async def mock_result(*args, **kwargs):
    return {'msgs': 3, 'words': 5}

if __name__ == '__main__':
    nose.run(defaultTest=__name__)