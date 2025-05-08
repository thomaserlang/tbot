from fastapi import APIRouter

from .routes import (
    queue_events_route,
    queue_routes,
    queue_viewer_routes,
)

channel_queue_router = APIRouter(tags=['Channel Queue'])
channel_queue_router.include_router(queue_routes.router)
channel_queue_router.include_router(queue_viewer_routes.router)
channel_queue_router.include_router(queue_events_route.router)
