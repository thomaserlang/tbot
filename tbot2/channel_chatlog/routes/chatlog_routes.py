from datetime import datetime
from typing import Annotated, cast
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Query, Security, WebSocket, WebSocketDisconnect

from tbot2.common import ChatMessage, Provider, TAccessLevel, TokenData
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
    provider: Annotated[Provider | None, Query()] = None,
    provider_viewer_id: str | None = None,
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

    if provider and provider_viewer_id:
        stmt = stmt.where(
            MChatlog.provider == provider,
            MChatlog.provider_viewer_id == provider_viewer_id,
        )

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
    provider: Annotated[Provider | None, Query()] = None,
    provider_viewer_id: str | None = None,
) -> None:
    await websocket.accept()
    async with database.redis.pubsub() as pubsub:  # type: ignore
        await pubsub.subscribe(f'tbot:live_chat:{channel_id}')  # type: ignore
        while True:
            data = cast(
                dict[str, str],
                await pubsub.get_message(  # type: ignore
                    ignore_subscribe_messages=True,
                    timeout=None,  # type: ignore
                ),
            )
            if not data:
                continue
            try:
                message = ChatMessage.model_validate_json(data['data'])
                if provider and provider_viewer_id:
                    if (
                        message.provider != provider
                        or message.provider_viewer_id != provider_viewer_id
                    ):
                        continue
                await websocket.send_text(message.model_dump_json())
            except WebSocketDisconnect:
                return
            except RuntimeError:
                return
