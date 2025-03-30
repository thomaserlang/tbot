from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from tbot2.auth_backend import AuthBackend
from tbot2.channel.router import channel_router
from tbot2.channel_chat_filters.router import chat_filter_router
from tbot2.channel_quote.router import channel_quotes_router
from tbot2.command.router import command_router
from tbot2.config_settings import config
from tbot2.database import database
from tbot2.spotify.router import spotify_router
from tbot2.twitch.router import twitch_router
from tbot2.user.router import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.setup()
    yield
    await database.close()


app = FastAPI(title='TBOT API', version='2.0', lifespan=lifespan)
app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(config.web.base_url)],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(twitch_router, prefix='/api/2')
app.include_router(channel_quotes_router, prefix='/api/2')
app.include_router(command_router, prefix='/api/2')
app.include_router(chat_filter_router, prefix='/api/2')
app.include_router(user_router, prefix='/api/2')
app.include_router(spotify_router, prefix='/api/2')
app.include_router(channel_router, prefix='/api/2')
