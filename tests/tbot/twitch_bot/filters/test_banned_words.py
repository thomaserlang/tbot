import unittest
import tbot.testbase
from tbot import utils
import logging

class Test_banned_words(unittest.TestCase):

    def test_check_message(self):
        self.assertTrue(utils.check_message(
            'Lorem ipsum dolor sit amet, ad Stupid message errem dolores reprimique pri',
            ['stupid'],
        ))
        self.assertFalse(utils.check_message(
            'Lorem ipsum dolor sit amet, ad Stupid message errem dolores reprimique pri',
            ['stupidd'],
        )) 
        self.assertFalse(utils.check_message(
            'Lorem ipsum dolor sit amet, ad Stupid message errem dolores reprimique pri',
            ['this is stupid'],
        )) 
        self.assertFalse(utils.check_message(
            'Lorem ipsum dolor sit amet, ad Stupidity message errem dolores reprimique pri',
            ['stupid'],
        ))
        self.assertTrue(utils.check_message(
            'stupid Lorem ipsum dolor sit amet, ad message errem dolores reprimique pri',
            ['message stupid'],
        ))
        self.assertTrue(utils.check_message(
            'Lorem ipsum dolor sit amet, ad stupid message errem dolores reprimique pri',
            ['"stupid message"'],
        ))       
        self.assertFalse(utils.check_message(
            'Lorem ipsum dolor sit amet, ad stupid message errem dolores reprimique pri',
            ['"test stupid message"'],
        ))
        self.assertFalse(utils.check_message(
            'Lorem ipsum dolor sit amet, ad stupid message errem dolores reprimique pri',
            ['test stupid message'],
        ))
        self.assertTrue(utils.check_message(
            'Lorem ipsum dolor sit amet, ad stupid message errem dolores reprimique pri',
            ['re:st[ou]+pid'],
        ))
        self.assertTrue(utils.check_message(
            'Lorem ipsum dolor sit amet, ad stOOOupid message errem dolores reprimique pri',
            ['re:st[ou]+pid'],
        ))
        self.assertFalse(utils.check_message(
            'Lorem ipsum dolor sit amet, ad stoooopid message errem dolores reprimique pri',
            ['re:^st[ou]+pid'],
        ))
        self.assertTrue(utils.check_message(
            'Lorem ipsum dolor sit amet, ad stoooopid message errem dolores reprimique pri',
            ['re:^st[ou]+pid|amet'],
        ))

if __name__ == '__main__':
    tbot.testbase.run_file(__file__)