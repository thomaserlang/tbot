import unittest, nose, re, logging
from tbot.utils import link

class Test(unittest.TestCase):

    def test_link(self):

        self.assertEqual(link.find_links('not a link'), [])
        self.assertEqual(link.find_links('3.1'), [])
        self.assertEqual(link.find_links('3.'), [])
        self.assertEqual(link.find_links('test.'), [])
        self.assertEqual(link.find_links('test 3.1a'), [])
        self.assertEqual(link.find_links('127,123.4'), [])

        tests = [
            ('test.com', ('test.com', '', 'test.com', '', '')),
            ('test.net/test.html', ('test.net', '', 'test.net', '/test.html', '')),
            ('cs.money', ('cs.money', '', 'cs.money', '', '')),
            ('test.abbott', ('test.abbott', '', 'test.abbott', '', '')),
            ('test.abogado', ('test.abogado', '', 'test.abogado', '', '')),
            ('test.ac', ('test.ac', '', 'test.ac', '', '')),
        ]
        for t in tests:
            logging.info(t[0])
            self.assertEqual(
                link.find_links(t[0])[0],
                t[1],
            )

if __name__ == '__main__':
    nose.run(defaultTest=__name__)