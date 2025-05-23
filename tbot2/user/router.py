from fastapi import APIRouter

from .routes import me_routes, me_settings_routes

user_router = APIRouter(tags=['Me'])
user_router.include_router(me_routes.router)
user_router.include_router(me_settings_routes.router)
