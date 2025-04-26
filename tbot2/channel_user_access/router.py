from fastapi import APIRouter

from .routes import channel_user_access_routes, channel_user_invite_routes

channel_user_access_router = APIRouter(tags=['Channel User Invite'])
channel_user_access_router.include_router(
    channel_user_invite_routes.router,
)
channel_user_access_router.include_router(
    channel_user_access_routes.router,
)
