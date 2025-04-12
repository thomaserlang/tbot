from fastapi import APIRouter

from .routes import (
    channel_chat_message_event_route,
    stream_online_offline_event_route,
    twitch_oauth_routes,
)

twitch_router = APIRouter()
twitch_router.include_router(twitch_oauth_routes.router, include_in_schema=False)
twitch_router.include_router(
    channel_chat_message_event_route.router, include_in_schema=False
)
twitch_router.include_router(
    stream_online_offline_event_route.router, include_in_schema=False
)
