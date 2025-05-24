from datetime import datetime
from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Query, Security

from tbot2.common import (
    ChatMessage,
    ChatMessageType,
    Provider,
    TAccessLevel,
    TokenData,
)
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQueryDep, page_cursor

from ..models.chat_message_model import MChatMessage
from ..types import ChatMessageScope

router = APIRouter()


@router.get(
    '/channels/{channel_id}/chat-messages',
    name='Get Chat Messages',
)
async def get_chat_messages_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChatMessageScope.READ])
    ],
    page_query: PageCursorQueryDep,
    provider: Annotated[Provider | None, Query()] = None,
    provider_viewer_id: str | None = None,
    type: ChatMessageType | None = None,
    lte_created_at: datetime | None = None,
) -> PageCursor[ChatMessage]:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    stmt = (
        sa.select(MChatMessage)
        .where(
            MChatMessage.channel_id == channel_id,
        )
        .order_by(MChatMessage.id.desc())
    )

    if provider and provider_viewer_id:
        stmt = stmt.where(
            MChatMessage.provider == provider,
            MChatMessage.provider_viewer_id == provider_viewer_id,
        )

    if lte_created_at:
        stmt = stmt.where(MChatMessage.created_at <= lte_created_at)

    if type:
        stmt = stmt.where(MChatMessage.type == type)

    return await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=ChatMessage,
        count_total=False,
    )
