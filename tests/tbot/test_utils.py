import unittest, nose
from tbot import utils

class test_utils(unittest.TestCase):

    def test_seconds_to_pretty(self):
        self.assertEqual('0 seconds', utils.seconds_to_pretty(0))
        self.assertEqual('1 second', utils.seconds_to_pretty(1))
        self.assertEqual('30 seconds', utils.seconds_to_pretty(30))
        self.assertEqual('1 minute', utils.seconds_to_pretty(60))
        self.assertEqual('1 minute and 1 second', utils.seconds_to_pretty(61))
        self.assertEqual('1 hour', utils.seconds_to_pretty(3600))
        self.assertEqual('1 hour and 3 seconds', utils.seconds_to_pretty(3603))
        self.assertEqual('1 hour and 1 minute', utils.seconds_to_pretty(3660))
        self.assertEqual('1 hour and 2 minutes', utils.seconds_to_pretty(3720))
        self.assertEqual('1 day', utils.seconds_to_pretty(3600*24))
        self.assertEqual('1 day and 2 seconds', utils.seconds_to_pretty((3600*24)+2))
        self.assertEqual('1 day, 1 hour and 15 minutes', utils.seconds_to_pretty((3600*24)+3600+900))
        self.assertEqual('1 day, 1 hour and 15 minutes', utils.seconds_to_pretty((3600*24)+3600+900))
        self.assertEqual('1 month, 1 hour and 15 minutes', utils.seconds_to_pretty((30*(3600*24))+3600+900))
        self.assertEqual('1 year, 1 hour and 15 minutes', utils.seconds_to_pretty(12*(30*(3600*24))+3600+900))
        self.assertEqual('1 year, 1 month and 13 days', utils.seconds_to_pretty(13*(31*(3600*24))+3600+900))

    def test_twitch_remove_emotes(self):
        message = 'test bahIdk 123 Kappa :) SeriousSloth asd bahIdk'
        emotes = '321674:5-10,42-47/25:16-20/1:22-23/81249:25-36'
        m = utils.twitch_remove_emotes(message, emotes)
        self.assertEqual(m, 'test 123 asd')

        message = 'bahIdk'
        emotes = '321674:0-5'
        m = utils.twitch_remove_emotes(message, emotes)
        self.assertEqual(m, '')

        message = 'bahIdk this is a test'
        emotes = '321674:0-5'
        m = utils.twitch_remove_emotes(message, emotes)
        self.assertEqual(m, 'this is a test')

if __name__ == '__main__':
    nose.run(defaultTest=__name__)