from fastapi import APIRouter

from .routes import activity_routes, activity_type_routes, activity_ws_route

channel_activity_router = APIRouter(tags=['Channel Activity'])
channel_activity_router.include_router(activity_routes.router)
channel_activity_router.include_router(activity_type_routes.router)
channel_activity_router.include_router(activity_ws_route.router)
