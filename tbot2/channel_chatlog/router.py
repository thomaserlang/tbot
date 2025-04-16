from fastapi import APIRouter

from .routes import chatlog_routes

chatlog_router = APIRouter(tags=['Chatlogs'])
chatlog_router.include_router(chatlog_routes.router)
