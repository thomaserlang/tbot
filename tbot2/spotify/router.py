from fastapi import APIRouter

from .routes import spotify_oauth_routes

spotify_router = APIRouter(tags=['Spotify'])
spotify_router.include_router(spotify_oauth_routes.router, include_in_schema=False)
