from tornado import web
from tbot.web.handlers.base import Base_handler
from tbot import utils

class Api_handler(Base_handler):

    def initialize(self):
        self.access_token = None
        if self.request.body:
            try:
                self.request.body = utils.json_loads(self.request.body)
            except ValueError:
                self.request.body = {}
        else:
            self.request.body = {}

    def write_object(self, obj):
        self.write(
            utils.json_dumps(obj, indent=4, sort_keys=True),
        )

    def set_default_headers(self):
        self.set_header('Cache-Control', 'no-cache, must-revalidate')
        self.set_header('Expires', 'Sat, 26 Jul 1997 05:00:00 GMT')
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Authorization, Content-Type, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, X-Requested-With')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE')
        self.set_header('Access-Control-Expose-Headers', 'ETag, Link, X-Total-Count, X-Total-Pages, X-Page')
        self.set_header('Access-Control-Max-Age', '86400')
        self.set_header('Access-Control-Allow-Credentials', 'true')