from fastapi import APIRouter

from .routes import (
    event_channel_chat_message_route,
    event_channel_chat_notification_route,
    event_channel_moderate_route,
    event_channel_subscription_gift_route,
    event_channel_update_route,
    event_stream_online_offline_route,
    twitch_badges_route,
    twitch_oauth_routes,
)

twitch_eventsub_router = APIRouter(prefix='/twitch/eventsub', include_in_schema=False)
twitch_eventsub_router.include_router(event_channel_chat_message_route.router)
twitch_eventsub_router.include_router(event_channel_chat_notification_route.router)
twitch_eventsub_router.include_router(event_stream_online_offline_route.router)
twitch_eventsub_router.include_router(event_channel_moderate_route.router)
twitch_eventsub_router.include_router(event_channel_update_route.router)
twitch_eventsub_router.include_router(event_channel_subscription_gift_route.router)

twitch_router = APIRouter()
twitch_router.include_router(twitch_eventsub_router)
twitch_router.include_router(twitch_oauth_routes.router, include_in_schema=False)
twitch_router.include_router(twitch_badges_route.router, include_in_schema=False)
