import asyncio
from datetime import datetime
from typing import Annotated, cast
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Query, Security, WebSocket, WebSocketDisconnect
from loguru import logger

from tbot2.common import ChatMessage, ChatMessageType, Provider, TAccessLevel, TokenData
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
    type: ChatMessageType | None = None,
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

    if type:
        stmt = stmt.where(MChatlog.type == type)

    page = await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=Chatlog,
        count_total=False,
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
    type: ChatMessageType | None = None,
) -> None:
    await websocket.accept()
    _, pending = await asyncio.wait(
        [
            asyncio.create_task(handle_disconnect(websocket)),
            asyncio.create_task(
                handle_connection(
                    channel_id=channel_id,
                    websocket=websocket,
                    provider=provider,
                    provider_viewer_id=provider_viewer_id,
                    type=type,
                ),
            ),
        ],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


@logger.catch
async def handle_disconnect(
    websocket: WebSocket,
) -> None:
    while True:
        try:
            await websocket.receive_text()
        except WebSocketDisconnect:
            return


@logger.catch
async def handle_connection(
    channel_id: UUID,
    websocket: WebSocket,
    provider: Annotated[Provider | None, Query()] = None,
    provider_viewer_id: str | None = None,
    type: ChatMessageType | None = None,
) -> None:
    async with database.redis.pubsub() as pubsub:  # type: ignore
        await pubsub.subscribe(f'tbot:live_chat:{channel_id}')  # type: ignore
        while True:
            try:
                data = cast(
                    dict[str, str],
                    await pubsub.get_message(
                        ignore_subscribe_messages=True,
                        timeout=None,
                    ),
                )
                if not data:
                    continue

                message = ChatMessage.model_validate_json(data['data'])
                if provider and provider_viewer_id:
                    if (
                        message.provider != provider
                        or message.provider_viewer_id != provider_viewer_id
                    ):
                        continue
                if type and message.type != type:
                    continue

                await websocket.send_text(message.model_dump_json())
            except RuntimeError:
                return
