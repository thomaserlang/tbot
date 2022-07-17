from .base import Api_handler
from tbot import config

class Handler(Api_handler):

    def get(self):
        self.post() 

    def post(self):
        if self.get_argument('name') in config.data.rtmp_keys:
            self.set_status(200)
        else:
            self.set_status(401)