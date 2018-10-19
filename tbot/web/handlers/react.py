from tornado.web import RequestHandler

class Handler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render('react.html')