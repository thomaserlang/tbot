from fastapi import APIRouter

from .routes import chat_message_routes, chat_message_ws_route

chat_message_router = APIRouter(tags=['Chat Messages'])
chat_message_router.include_router(chat_message_routes.router)
chat_message_router.include_router(chat_message_ws_route.router)
