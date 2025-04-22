from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request, Response
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from tbot2.auth_backend import AuthBackend
from tbot2.bot_providers.router import bot_provider_routes
from tbot2.channel.router import channel_router
from tbot2.channel_chat_filters.router import chat_filter_router
from tbot2.channel_chatlog.router import chatlog_router
from tbot2.channel_command.router import command_router
from tbot2.channel_quote.router import channel_quotes_router
from tbot2.channel_timer.router import channel_timer_router
from tbot2.channel_viewer.router import channel_stats_router
from tbot2.config_settings import config
from tbot2.constants import APP_TITLE
from tbot2.database import database
from tbot2.dependecies import PlainResponse
from tbot2.setup_logger import setup_logger
from tbot2.spotify.router import spotify_router
from tbot2.twitch.router import twitch_router
from tbot2.user.router import user_router
from tbot2.youtube.router import youtube_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    setup_logger()
    await database.setup()
    yield
    await database.close()


app = FastAPI(
    title=f'{APP_TITLE} API',
    docs_url='/api/2/redoc',
    version='2.0',
    lifespan=lifespan,
)
app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(config.base_url)],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(PlainResponse)
async def plain_response_handler(_: Request, exc: PlainResponse) -> Response:
    return Response(
        content=exc.content,
        status_code=exc.status_code,
    )


app.include_router(twitch_router, prefix='/api/2')
app.include_router(channel_quotes_router, prefix='/api/2')
app.include_router(command_router, prefix='/api/2')
app.include_router(chat_filter_router, prefix='/api/2')
app.include_router(user_router, prefix='/api/2')
app.include_router(spotify_router, prefix='/api/2')
app.include_router(channel_router, prefix='/api/2')
app.include_router(channel_timer_router, prefix='/api/2')
app.include_router(bot_provider_routes, prefix='/api/2')
app.include_router(chatlog_router, prefix='/api/2')
app.include_router(channel_stats_router, prefix='/api/2')
app.include_router(youtube_router, prefix='/api/2')
