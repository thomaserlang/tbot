from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request, Response
from fastapi.concurrency import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.middleware.authentication import AuthenticationMiddleware

from tbot2.auth_backend import AuthBackend
from tbot2.bot_providers.router import bot_provider_routes
from tbot2.channel.router import channel_router
from tbot2.channel_chat_filters.router import chat_filter_router
from tbot2.channel_chatlog.router import chatlog_router
from tbot2.channel_command.router import command_router
from tbot2.channel_gambling.router import channel_gambling_router
from tbot2.channel_points.router import channel_point_settings_router
from tbot2.channel_provider.router import channel_provider_router
from tbot2.channel_queue.router import channel_queue_router
from tbot2.channel_quote.router import channel_quotes_router
from tbot2.channel_timer.router import channel_timer_router
from tbot2.channel_user_access.router import channel_user_access_router
from tbot2.channel_viewer.router import channel_stats_router
from tbot2.common import Error, TBotBaseException
from tbot2.common.constants import APP_TITLE
from tbot2.common.utils.pydantic_response import request_validation_error_to_error
from tbot2.config_settings import config
from tbot2.database import database
from tbot2.dependecies import PlainResponse
from tbot2.health.router import health_router
from tbot2.spotify.router import spotify_router
from tbot2.tiktok.router import tiktok_router
from tbot2.twitch.router import twitch_router
from tbot2.user.router import user_router
from tbot2.youtube.router import youtube_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await database.setup()
    yield
    await database.close()


app = FastAPI(
    title=f'{APP_TITLE} API',
    redoc_url='/api/2/docs',
    openapi_url='/api/2/openapi.json',
    version='2.0',
    lifespan=lifespan,
    responses={
        422: {
            'model': Error,
            'description': 'Validation error',
        },
        500: {
            'model': Error,
            'description': 'Internal server error',
        },
        400: {
            'model': Error,
            'description': 'Bad request',
        },
        401: {
            'model': Error,
            'description': 'Unauthorized',
        },
        403: {
            'model': Error,
            'description': 'Forbidden',
        },
        404: {
            'model': Error,
            'description': 'Not found',
        },
    },
)
app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(config.base_url)],
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
app.include_router(channel_timer_router, prefix='/api/2')
app.include_router(channel_stats_router, prefix='/api/2')
app.include_router(channel_provider_router, prefix='/api/2')
app.include_router(channel_user_access_router, prefix='/api/2')
app.include_router(channel_point_settings_router, prefix='/api/2')
app.include_router(channel_gambling_router, prefix='/api/2')
app.include_router(channel_queue_router, prefix='/api/2')
app.include_router(bot_provider_routes, prefix='/api/2')
app.include_router(chatlog_router, prefix='/api/2')
app.include_router(youtube_router, prefix='/api/2')
app.include_router(tiktok_router, prefix='/api/2')
app.include_router(health_router)


@app.exception_handler(PlainResponse)
async def plain_response_handler(_: Request, exc: PlainResponse) -> Response:
    return Response(
        content=exc.content,
        status_code=exc.status_code,
    )


@app.exception_handler(TBotBaseException)
async def api_error(request: Request, exc: TBotBaseException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.code,
        content=Error(
            code=exc.code,
            message=exc.message,
            type=exc.type,
            errors=exc.errors,
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=request_validation_error_to_error(exc).model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=Error(
            code=500,
            message='Internal server error',
            type='internal_server_error',
            errors=[],
        ).model_dump(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=Error(
            code=exc.status_code,
            message=exc.detail,
            type='',
            errors=[],
        ).model_dump(),
    )
