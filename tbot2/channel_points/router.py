from fastapi import APIRouter

from .routes import channel_point_settings_route

channel_point_settings_router = APIRouter(tags=['Channel Point Settings'])
channel_point_settings_router.include_router(
    channel_point_settings_route.router,
)
