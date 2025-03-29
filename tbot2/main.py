from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from tbot2.auth_backend import AuthBackend
from tbot2.channel_chat_filters.router import chat_filter_router
from tbot2.channel_quote.router import channel_quotes_router
from tbot2.command.router import command_router
from tbot2.contexts import asynccontextmanager
from tbot2.database import database
from tbot2.twitch.router import twitch_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.setup()
    yield
    await database.close()


app = FastAPI(title='TBOT API', version='2.0', lifespan=lifespan)
app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())

app.include_router(twitch_router)
app.include_router(channel_quotes_router, prefix='/api/2')
app.include_router(command_router, prefix='/api/2')
app.include_router(chat_filter_router, prefix='/api/2')
