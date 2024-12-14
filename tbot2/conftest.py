import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from tbot2.database import database
from tbot2.main import app


@pytest_asyncio.fixture(scope='function')  # type: ignore
async def client():
    await database.setup_test()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac
    await database.close_test()


@pytest_asyncio.fixture(scope='function')  # type: ignore
async def db():
    await database.setup_test()
    yield
    await database.close_test()