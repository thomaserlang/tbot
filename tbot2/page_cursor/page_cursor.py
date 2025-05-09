import base64
from typing import Any, TypeVar, overload

import sqlalchemy as sa
from pydantic import BaseModel
from sqlakeyset.asyncio import select_page  # type: ignore

from tbot2.contexts import AsyncSession, get_session

from .schemas import PageCursor, PageCursorQuery

T = TypeVar('T', bound=BaseModel)
_TP = TypeVar('_TP', bound=tuple[Any, ...])


@overload
async def page_cursor(
    query: sa.Select[_TP],
    page_query: PageCursorQuery,
    response_model: type[T],
    session: AsyncSession | None = None,
    count_total: bool = True,
) -> PageCursor[T]: ...


@overload
async def page_cursor(
    query: sa.Select[_TP],
    page_query: PageCursorQuery,
    response_model: None = None,
    session: AsyncSession | None = None,
) -> PageCursor[Any]: ...


async def page_cursor(
    query: sa.Select[_TP],
    page_query: PageCursorQuery,
    response_model: Any | None = None,
    session: AsyncSession | None = None,
    count_total: bool = True,
) -> PageCursor[Any]:
    async with get_session(session) as session:
        page = await select_page(
            s=session,
            selectable=query,
            per_page=page_query.per_page,
            page=base64.urlsafe_b64decode(page_query.cursor).decode()
            if page_query.cursor
            else None,
        )
        cursor = (
            base64.urlsafe_b64encode(page.paging.bookmark_next.encode()).decode()
            if page.paging.has_next
            else None
        )

        count_subquery = query.order_by(None).options(sa.orm.noload('*')).subquery()

        total = None
        if count_total:
            total = await session.scalar(
                sa.Select[_TP](sa.func.count(sa.literal_column('*'))).select_from(
                    count_subquery
                )
            )

            if total is None:
                total = 0

        if response_model:
            return PageCursor(
                records=[
                    response_model.model_validate(row[0]) for row in page.paging.rows
                ],
                cursor=cursor,
                total=total,
            )
        return PageCursor(
            records=page.paging.rows,
            cursor=cursor,
            total=total,
        )
