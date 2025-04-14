from datetime import datetime
from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Security, WebSocket, WebSocketDisconnect

from tbot2.common import TAccessLevel, TokenData
from tbot2.database import database
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQueryDep, page_cursor

from ..models.chatlog_model import MChatlog
from ..schemas.chatlog_schema import Chatlog
from ..types import ChatlogsScope

router = APIRouter()


@router.get(
    '/channels/{channel_id}/chatlogs',
    name='Get Chatlogs',
)
async def get_chatlogs(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChatlogsScope.READ])
    ],
    page_query: PageCursorQueryDep,
    chatter_id: str | None = None,
    lte_created_at: datetime | None = None,
) -> PageCursor[Chatlog]:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    stmt = (
        sa.select(MChatlog)
        .where(
            MChatlog.channel_id == channel_id,
        )
        .order_by(MChatlog.id.desc())
    )

    if chatter_id:
        stmt = stmt.where(MChatlog.chatter_id == chatter_id)

    if lte_created_at:
        stmt = stmt.where(MChatlog.created_at <= lte_created_at)

    page = await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=Chatlog,
    )
    return page


@router.websocket(
    '/channels/{channel_id}/chat-ws',
    name='Get Chatlogs Websocket',
)
async def get_chat_ws_route(
    *,
    websocket: WebSocket,
    channel_id: UUID,
) -> None:
    await websocket.accept()

    async with database.redis.pubsub() as pubsub:  # type: ignore
        await pubsub.subscribe(f'tbot:live_chat:{channel_id}')  # type: ignore
        while True:
            message = await pubsub.get_message(  # type: ignore
                ignore_subscribe_messages=True,
                timeout=None,  # type: ignore
            )
            if not message:
                continue
            try:
                await websocket.send_text(message['data'])  # type: ignore
            except WebSocketDisconnect:
                pass
            except RuntimeError:
                pass
