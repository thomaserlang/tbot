from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from tbot2.config_settings import config

from .twitch.router import twitch_router

app = FastAPI(title='TBOT API', version='2.0')
app.add_middleware(SessionMiddleware, secret_key=config.web.cookie_secret)
app.include_router(twitch_router)
