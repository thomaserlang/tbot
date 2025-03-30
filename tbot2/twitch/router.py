from fastapi import APIRouter

from .eventsub.router import eventsub_router
from .routes import twitch_oauth_routes

twitch_router = APIRouter()
twitch_router.include_router(eventsub_router, include_in_schema=False)
twitch_router.include_router(twitch_oauth_routes.router, include_in_schema=False)
