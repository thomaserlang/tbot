from fastapi import APIRouter

from .routes import youtube_oauth_router

youtube_router = APIRouter()
youtube_router.include_router(youtube_oauth_router.router, include_in_schema=False)
