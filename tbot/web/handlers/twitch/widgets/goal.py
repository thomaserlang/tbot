from tornado.web import RequestHandler

class Handler(RequestHandler):

    def get(self, key, *args, **kwargs):
        self.render('twitch/widgets/goal.html', key=key)