from .base import Base_handler

class Handler(Base_handler):

    def get(self):
        _next = self.get_argument('next', None)
        self.clear_cookie('next')
        if _next:
            self.set_secure_cookie('next', _next, expires_days=None)
        self.render('login.html')