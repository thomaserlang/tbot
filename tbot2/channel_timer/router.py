from fastapi import APIRouter

from .routes import timer_routes

channel_timer_router = APIRouter(
    tags=['Channel Timer'],
)
channel_timer_router.include_router(
    timer_routes.router,
)
