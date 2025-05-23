from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Security
from uuid6 import uuid7

from tbot2.channel_chat_filters.models.chat_filter_model import MChatFilter
from tbot2.common import ChatMessageCreate, ErrorMessage, TAccessLevel, TokenData
from tbot2.dependecies import Depends, authenticated
from tbot2.page_cursor import PageCursor, PageCursorQuery, page_cursor

from ..actions.banned_term_actions import (
    create_banned_term,
    delete_banned_term,
    get_banned_term,
    update_banned_term,
)
from ..actions.chat_filter_actions import get_chat_filter
from ..filters.banned_terms_filter import ChatFilterBannedTerms, FilterMatchResult
from ..models.chat_filter_banned_terms_model import MChatFilterBannedTerm
from ..schemas.banned_term_schema import (
    BannedTerm,
    BannedTermCreate,
    BannedTermTest,
    BannedTermUpdate,
)
from ..types import ChatFilterScope

router = APIRouter()


@router.get(
    '/channels/{channel_id}/chat-filters/{filter_id}/banned-terms',
    name='Get Banned Terms',
)
async def get_banned_terms_route(
    channel_id: UUID,
    filter_id: UUID,
    page_query: Annotated[PageCursorQuery, Depends()],
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChatFilterScope.READ])
    ],
) -> PageCursor[BannedTerm]:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    stmt = (
        sa.select(
            MChatFilterBannedTerm,
        )
        .where(
            MChatFilterBannedTerm.chat_filter_id == filter_id,
            MChatFilter.id == MChatFilterBannedTerm.chat_filter_id,
            MChatFilter.channel_id == channel_id,
        )
        .order_by(
            MChatFilterBannedTerm.id,
        )
    )

    page = await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=BannedTerm,
    )

    return page


@router.get(
    '/channels/{channel_id}/chat-filters/{filter_id}/banned-terms/{banned_term_id}',
    name='Get Banned Term',
)
async def get_banned_term_route(
    channel_id: UUID,
    filter_id: UUID,
    banned_term_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChatFilterScope.READ])
    ],
) -> BannedTerm:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    term = await get_banned_term(
        term_id=banned_term_id,
    )
    if not term:
        raise ErrorMessage(
            'Banned term not found', code=404, type='banned_term_not_found'
        )

    filter = await get_chat_filter(
        filter_id=filter_id,
    )
    if not filter or filter.channel_id != channel_id:
        raise ErrorMessage(
            'Chat filter not found', code=404, type='chat_filter_not_found'
        )

    return term


@router.post(
    '/channels/{channel_id}/chat-filters/{filter_id}/banned-terms',
    name='Create Banned Term',
    status_code=201,
)
async def create_banned_term_route(
    channel_id: UUID,
    filter_id: UUID,
    data: BannedTermCreate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChatFilterScope.WRITE])
    ],
) -> BannedTerm:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    filter = await get_chat_filter(
        filter_id=filter_id,
    )
    if not filter or filter.channel_id != channel_id:
        raise ErrorMessage(
            'Chat filter not found', code=404, type='chat_filter_not_found'
        )

    term = await create_banned_term(
        filter_id=filter.id,
        data=data,
    )

    return term


@router.put(
    '/channels/{channel_id}/chat-filters/{filter_id}/banned-terms/{banned_term_id}',
    name='Update Banned Term',
)
async def update_banned_term_route(
    channel_id: UUID,
    filter_id: UUID,
    banned_term_id: UUID,
    data: BannedTermUpdate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChatFilterScope.WRITE])
    ],
) -> BannedTerm:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    filter = await get_chat_filter(
        filter_id=filter_id,
    )
    if not filter or filter.channel_id != channel_id:
        raise ErrorMessage(
            'Chat filter not found', code=404, type='chat_filter_not_found'
        )

    term = await get_banned_term(
        term_id=banned_term_id,
    )
    if not term:
        raise ErrorMessage(
            'Banned term not found', code=404, type='banned_term_not_found'
        )

    term = await update_banned_term(
        term_id=banned_term_id,
        data=data,
    )

    return term


@router.delete(
    '/channels/{channel_id}/chat-filters/{filter_id}/banned-terms/{banned_term_id}',
    name='Delete Banned Term',
    status_code=204,
)
async def delete_banned_term_route(
    channel_id: UUID,
    filter_id: UUID,
    banned_term_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChatFilterScope.WRITE])
    ],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    filter = await get_chat_filter(
        filter_id=filter_id,
    )
    if not filter or filter.channel_id != channel_id:
        raise ErrorMessage(
            'Chat filter not found', code=404, type='chat_filter_not_found'
        )

    await delete_banned_term(
        term_id=banned_term_id,
    )


@router.post(
    '/channels/{channel_id}/chat-filters/{filter_id}/banned-terms/test',
    name='Test Banned Term',
)
async def banned_term_test_route(
    channel_id: UUID,
    filter_id: UUID,
    data: BannedTermTest,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChatFilterScope.WRITE])
    ],
) -> FilterMatchResult:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    filter = await get_chat_filter(
        filter_id=filter_id,
        model=ChatFilterBannedTerms,
    )
    if not filter or filter.channel_id != channel_id:
        raise ErrorMessage(
            'Chat filter not found', code=404, type='chat_filter_not_found'
        )

    result = await filter.check_message(
        message=ChatMessageCreate(
            id=uuid7(),
            type='message',
            created_at=datetime.now(tz=UTC),
            provider='twitch',
            provider_channel_id='test',
            channel_id=channel_id,
            provider_viewer_id='test',
            viewer_name='test',
            viewer_display_name='test',
            message=data.message,
            provider_message_id='test',
        )
    )
    return result
