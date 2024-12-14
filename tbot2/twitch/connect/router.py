from fastapi import APIRouter

from .routes.connect_twitch_bot_route import router as connect_twitch_bot_router

connect_router = APIRouter()
connect_router.include_router(connect_twitch_bot_router)
