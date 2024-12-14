from fastapi import APIRouter

from .connect.router import connect_router
from .eventsub.router import eventsub_router

twitch_router = APIRouter()
twitch_router.include_router(eventsub_router, prefix='/twitch', include_in_schema=False)
twitch_router.include_router(connect_router, prefix='/twitch')
