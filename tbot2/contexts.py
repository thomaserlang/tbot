from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from .database import AsyncSession, conn


@asynccontextmanager
async def get_session(
    session: AsyncSession | None = None,
) -> AsyncGenerator[AsyncSession]:
    if session:
        yield session
    else:
        async with conn.session() as session:
            yield session
            await session.commit()
