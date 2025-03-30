from fastapi import APIRouter

from .routes import channel_provider_routes, channel_routes

channel_router = APIRouter(tags=['Channel'])
channel_router.include_router(channel_routes.router)
channel_router.include_router(channel_provider_routes.router)
