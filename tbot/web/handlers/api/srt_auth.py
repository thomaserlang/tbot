from .base import Api_handler
from tbot import config
class Handler(Api_handler):

    def post(self):
        if self.get_argument('on_event') == 'on_connect':
            s = self.get_argument('srt_url', '').rsplit('/', 1)
            if len(s) == 2:
                if s[1] in config.data.rtmp_keys:
                    self.set_status(200)
                    return
        self.set_status(401)