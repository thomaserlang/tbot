from fastapi import APIRouter

from .routes.channel_chat_message_route import router as channel_chat_message_router

eventsub_router = APIRouter(prefix='/twitch/eventsub')
eventsub_router.include_router(channel_chat_message_router)
