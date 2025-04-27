from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, Security

from tbot2.channel_quote.types import TChannelQuoteScope
from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQuery, page_cursor

from ..actions.channel_quote_actions import (
    ChannelQuoteCreate,
    ChannelQuoteUpdate,
    create_channel_quote,
    delete_channel_quote,
    get_channel_quote,
    get_channel_quote_by_number,
    update_channel_quote,
)
from ..models.channel_quote_model import MChannelQuote
from ..schemas.channel_quote_schema import ChannelQuote

router = APIRouter()


@router.get(
    '/channels/{channel_id}/quotes',
    name='Get Channel Quotes',
)
async def get_channel_quotes_route(
    channel_id: UUID,
    page: Annotated[PageCursorQuery, Depends()],
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[TChannelQuoteScope.READ])
    ],
) -> PageCursor[ChannelQuote]:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    stmt = (
        sa.select(MChannelQuote)
        .where(
            MChannelQuote.channel_id == channel_id,
        )
        .order_by(MChannelQuote.number.desc())
    )

    return await page_cursor(
        query=stmt,
        page_query=page,
        response_model=ChannelQuote,
    )


@router.get(
    '/channels/{channel_id}/quotes/{quote_id}',
    name='Get Channel Quote',
)
async def get_channel_quote_route(
    channel_id: UUID,
    quote_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[TChannelQuoteScope.READ])
    ],
) -> ChannelQuote:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    quote = await get_channel_quote(
        quote_id=quote_id,
    )
    if not quote:
        raise HTTPException(
            status_code=404,
            detail='Quote not found',
        )
    return quote


@router.get(
    '/channels/{channel_id}/quotes/number/{number}',
    name='Get Channel Quote By Number',
)
async def get_channel_quote_by_number_route(
    channel_id: UUID,
    number: int,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[TChannelQuoteScope.READ])
    ],
) -> ChannelQuote:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    quote = await get_channel_quote_by_number(
        channel_id=channel_id,
        number=number,
    )
    if not quote:
        raise HTTPException(
            status_code=404,
            detail='Quote not found',
        )
    return quote


@router.post(
    '/channels/{channel_id}/quotes',
    name='Create Channel Quote',
    status_code=201,
)
async def create_channel_quote_route(
    channel_id: UUID,
    data: ChannelQuoteCreate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[TChannelQuoteScope.WRITE])
    ],
) -> ChannelQuote:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    quote = await create_channel_quote(
        channel_id=channel_id,
        data=data,
    )
    return quote


@router.put(
    '/channels/{channel_id}/quotes/{quote_id}',
    name='Update Channel Quote',
)
async def update_channel_quote_route(
    channel_id: UUID,
    quote_id: UUID,
    data: ChannelQuoteUpdate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[TChannelQuoteScope.WRITE])
    ],
) -> ChannelQuote:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    quote = await get_channel_quote(
        quote_id=quote_id,
    )
    if not quote or quote.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail='Quote not found',
        )

    quote = await update_channel_quote(
        quote_id=quote_id,
        data=data,
    )
    return quote


@router.delete(
    '/channels/{channel_id}/quotes/{quote_id}',
    name='Delete Channel Quote',
    responses={
        204: {
            'model': None,
        },
    },
    status_code=204,
)
async def delete_channel_quote_route(
    channel_id: UUID,
    quote_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[TChannelQuoteScope.WRITE])
    ],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    quote = await get_channel_quote(
        quote_id=quote_id,
    )
    if not quote or quote.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail='Quote not found',
        )

    await delete_channel_quote(
        quote_id=quote_id,
    )
