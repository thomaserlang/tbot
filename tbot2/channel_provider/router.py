from fastapi import APIRouter

from .routes import channel_provider_routes

channel_provider_router = APIRouter(tags=['Channel Provider'])
channel_provider_router.include_router(channel_provider_routes.router)
