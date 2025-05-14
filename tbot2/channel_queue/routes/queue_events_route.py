import asyncio
from typing import Any, cast
from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger

from tbot2.database import conn

from ..actions.queue_publish_actions import queue_queue_key

router = APIRouter()


@router.websocket(
    '/channel-queues/{channel_queue_id}/events',
    name='Get Channel Queue Events',
)
async def get_queue_events_route(
    *,
    websocket: WebSocket,
    channel_queue_id: UUID,
) -> None:
    await websocket.accept()
    _, pending = await asyncio.wait(
        [
            asyncio.create_task(handle_disconnect(websocket)),
            asyncio.create_task(
                handle_event(channel_queue_id=channel_queue_id, websocket=websocket),
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


async def handle_event(
    channel_queue_id: UUID,
    websocket: WebSocket,
) -> None:
    async with conn.redis.pubsub() as pubsub:  # type: ignore
        await pubsub.subscribe(  # type: ignore
            queue_queue_key(channel_queue_id=channel_queue_id)
        )
        while True:
            try:
                data = cast(
                    dict[str, Any],
                    await pubsub.get_message(
                        ignore_subscribe_messages=True, timeout=None
                    ),
                )
                if not data:
                    continue

                await websocket.send_text(data['data'])
            except RuntimeError:
                return
