import asyncio
from typing import Annotated, cast
from uuid import UUID

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from loguru import logger

from tbot2.common import (
    ChatMessage,
    ChatMessageType,
    Provider,
    PubSubEvent,
)
from tbot2.database import conn

from ..actions.chat_message_actions import (
    chat_message_queue_key,
)

router = APIRouter()


@router.websocket(
    '/channels/{channel_id}/chat-messages-ws',
    name='Websocket Chat Messages',
)
async def ws_chat_messages_route(
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
    async with conn.redis.pubsub() as pubsub:  # type: ignore
        await pubsub.subscribe(chat_message_queue_key(channel_id=channel_id))  # type: ignore
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

                event = PubSubEvent[ChatMessage].model_validate_json(data['data'])
                if provider and provider_viewer_id:
                    if (
                        event.data.provider != provider
                        or event.data.provider_viewer_id != provider_viewer_id
                    ):
                        continue
                if type and event.data.type != type:
                    continue

                await websocket.send_text(event.model_dump_json())
            except RuntimeError:
                return
