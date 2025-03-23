from fastapi import APIRouter

from .routes import chat_filter_routes

chat_filter_router = APIRouter(tags=['Channel Chat Filters'])
chat_filter_router.include_router(chat_filter_routes.router)
