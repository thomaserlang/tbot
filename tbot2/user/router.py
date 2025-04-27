from fastapi import APIRouter

from .routes import me_routes

user_router = APIRouter()
user_router.include_router(me_routes.router, tags=['Me'])
