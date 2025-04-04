from fastapi import APIRouter

from .routes import command_routes

command_router = APIRouter()
command_router.include_router(command_routes.router, tags=['Commands'])
