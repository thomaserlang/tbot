from fastapi import APIRouter

from .routes import tiktok_oauth_routes, tiktok_username_route

tiktok_router = APIRouter(tags=['TikTok'])
tiktok_router.include_router(
    tiktok_oauth_routes.router,
    include_in_schema=False,
)
tiktok_router.include_router(
    tiktok_username_route.router,
)
