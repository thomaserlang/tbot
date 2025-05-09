from fastapi import APIRouter

from ..channel_viewer.routes import viewer_routes

channel_stats_router = APIRouter(tags=['Channel Viewer'])
channel_stats_router.include_router(viewer_routes.router)
