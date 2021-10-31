from .base import Api_handler, Api_exception
from tbot import config
import logging

class Handler(Api_handler):

    def get(self):
        self.post() 

    def post(self):
        if self.get_argument('name') in config['rtmp_keys']:
            self.set_status(200)
        else:
            self.set_status(401)