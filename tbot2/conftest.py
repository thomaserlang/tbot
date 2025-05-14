from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from tbot2.database import conn
from tbot2.main import app


@pytest_asyncio.fixture(scope='function')  # type: ignore
async def client() -> AsyncGenerator[AsyncClient]:
    await conn.setup_test()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac
    await conn.close_test()


@pytest_asyncio.fixture(scope='function')  # type: ignore
async def db() -> AsyncGenerator[None]:
    await conn.setup_test()
    yield
    await conn.close_test()
