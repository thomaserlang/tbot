from fastapi import APIRouter

from .routes import system_bot_provider_routes

bot_provider_routes = APIRouter(tags=['Bot Providers'])
bot_provider_routes.include_router(system_bot_provider_routes.router)
