from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from tbot2.auth_backend import AuthBackend
from tbot2.channel_quotes.router import channel_quotes_router
from tbot2.twitch.router import twitch_router

app = FastAPI(title='TBOT API', version='2.0')
app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())

app.include_router(twitch_router)
app.include_router(channel_quotes_router, prefix='/api/2')
