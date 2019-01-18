import unittest, nose
from tbot import utils

class Test_utils(unittest.TestCase):

    def test_seconds_to_pretty(self):
        self.assertEqual('0 seconds', utils.seconds_to_pretty(0))
        self.assertEqual('1 seconds', utils.seconds_to_pretty(1))
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
        self.assertEqual('1 year, 1 month, 13 days and 1 hour', utils.seconds_to_pretty(13*(31*(3600*24))+3600+900))

if __name__ == '__main__':
    nose.run(defaultTest=__name__)