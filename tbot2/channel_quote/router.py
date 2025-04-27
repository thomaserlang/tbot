from fastapi import APIRouter

from .routes import channel_quote_routes

channel_quotes_router = APIRouter()
channel_quotes_router.include_router(
    channel_quote_routes.router,
    tags=['Channel Quotes'],
)
