import asyncio
from typing import Annotated, cast
from uuid import UUID

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from loguru import logger

from tbot2.channel_activity.actions.activity_actions import (
    activity_queue_key,
)
from tbot2.common import PubSubEvent
from tbot2.common.utils.split_list_util import split_list
from tbot2.database import conn

from ..schemas.activity_schemas import Activity
from ..types.activity_types import ActivityType

router = APIRouter()


@router.websocket(
    '/channels/{channel_id}/activity-ws',
    name='Activity WebSocket',
)
async def ws_activity_route(
    *,
    websocket: WebSocket,
    channel_id: UUID,
    type: Annotated[list[ActivityType | str] | None, Query()] = None,
    not_type: Annotated[list[ActivityType | str] | None, Query()] = None,
    min_count: Annotated[
        list[str] | None, Query(description='<type>.<min count>')
    ] = None,
) -> None:
    await websocket.accept()
    _, pending = await asyncio.wait(
        [
            asyncio.create_task(handle_disconnect(websocket)),
            asyncio.create_task(
                handle_connection(
                    channel_id=channel_id,
                    websocket=websocket,
                    type=split_list(type) if type else None,
                    not_type=split_list(not_type) if not_type else None,
                    min_count=split_list(min_count) if min_count else None,
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
    type: list[ActivityType | str] | None = None,
    not_type: list[ActivityType | str] | None = None,
    min_count: Annotated[
        list[str] | None, Query(description='<type>.<min count>')
    ] = None,
) -> None:
    min_count_dict: dict[str, int] = {}
    if min_count:
        for item in min_count:
            type_str, count_str = item.split('.')
            count = int(count_str)
            min_count_dict[type_str] = count

    async with conn.redis.pubsub() as pubsub:  # type: ignore
        await pubsub.subscribe(activity_queue_key(channel_id=channel_id))  # type: ignore
        while True:
            try:
                data = cast(
                    dict[str, str],
                    await pubsub.get_message(
                        ignore_subscribe_messages=True, timeout=None
                    ),
                )
                if not data:
                    continue

                event = PubSubEvent[Activity].model_validate_json(data['data'])
                if type and event.data.type not in type:
                    continue

                if not_type and event.data.type in not_type:
                    continue

                if event.data.type in min_count_dict:
                    if event.data.count < min_count_dict[event.data.type]:
                        continue

                await websocket.send_text(event.model_dump_json())
            except RuntimeError:
                return
