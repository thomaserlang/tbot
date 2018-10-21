from tornado.web import RequestHandler
from tbot import config

class Handler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render('react.html', config=config)