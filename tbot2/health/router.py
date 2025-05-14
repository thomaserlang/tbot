import asyncio

import sqlalchemy as sa
from fastapi import APIRouter, Response

from tbot2.common import BaseSchema
from tbot2.contexts import get_session
from tbot2.database import conn

health_router = APIRouter()


class HealthResponse(BaseSchema):
    error: bool
    message: str
    service: str


@health_router.get(
    '/health',
    name='Health Check',
)
async def check_health(response: Response) -> list[HealthResponse]:
    result = await asyncio.gather(
        db_check(),
        redis_check(),
    )
    if any([r.error for r in result]):
        response.status_code = 500
    return [r for r in result]


async def db_check() -> HealthResponse:
    r = HealthResponse(
        error=False,
        message='OK',
        service='Database',
    )
    try:
        async with get_session() as s:
            await s.execute(sa.text('SELECT 1'))
    except Exception as e:
        r.error = True
        r.message = f'Error: {str(e)}'
    return r


async def redis_check() -> HealthResponse:
    r = HealthResponse(
        error=False,
        message='OK',
        service='Redis',
    )
    try:
        await conn.redis.ping()  # type: ignore
    except Exception as e:
        r.error = True
        r.message = f'Error: {str(e)}'
    return r
