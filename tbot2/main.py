from fastapi import FastAPI

from .twitch.router import twitch_router

app = FastAPI(title='TBOT API', version='2.0')
app.include_router(twitch_router)
