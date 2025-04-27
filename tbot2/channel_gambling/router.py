from fastapi import APIRouter

from .routes import (
    roulette_settings_routes,
    slots_settings_routes,
)

channel_gambling_router = APIRouter(tags=['Channel Gambling'])
channel_gambling_router.include_router(
    slots_settings_routes.router,
)
channel_gambling_router.include_router(
    roulette_settings_routes.router,
)
