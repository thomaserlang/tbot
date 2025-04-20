from fastapi import APIRouter

from .routes import youtube_create_broadcast_router, youtube_oauth_router

youtube_router = APIRouter(tags=['YouTube'])
youtube_router.include_router(youtube_oauth_router.router, include_in_schema=False)
youtube_router.include_router(youtube_create_broadcast_router.router)
