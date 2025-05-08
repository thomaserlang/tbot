from uuid import UUID

from tbot2.channel_queue.schemas.queue_event_schema import QueueEvent
from tbot2.database import database

from ..schemas.queue_viewer_schema import QueueViewer


def queue_event_key(*, channel_queue_id: UUID) -> str:
    return f'tbot:channel-queue:{channel_queue_id}'


async def publish_queue_viewer_created(
    channel_queue_viewer: QueueViewer,
) -> None:
    key = queue_event_key(channel_queue_id=channel_queue_viewer.channel_queue_id)
    event = QueueEvent(
        type='channel_queue_viewer_created',
        channel_queue_viewer=channel_queue_viewer,
    )
    await database.redis.publish(key, event.model_dump_json())  # type: ignore


async def publish_queue_viewer_deleted(
    channel_queue_viewer: QueueViewer,
) -> None:
    key = queue_event_key(channel_queue_id=channel_queue_viewer.channel_queue_id)
    event = QueueEvent(
        type='channel_queue_viewer_deleted',
        channel_queue_viewer=channel_queue_viewer,
    )
    await database.redis.publish(key, event.model_dump_json())  # type: ignore


async def publis_queue_viewer_moved(
    channel_queue_viewer: QueueViewer,
) -> None:
    key = queue_event_key(channel_queue_id=channel_queue_viewer.channel_queue_id)
    event = QueueEvent(
        type='channel_queue_viewer_moved',
        channel_queue_viewer=channel_queue_viewer,
    )
    await database.redis.publish(key, event.model_dump_json())  # type: ignore


async def publish_queue_cleared(channel_queue_id: UUID) -> None:
    key = queue_event_key(channel_queue_id=channel_queue_id)
    event = QueueEvent(
        type='channel_queue_cleared',
        channel_queue_viewer=None,
    )
    await database.redis.publish(key, event.model_dump_json())  # type: ignore
