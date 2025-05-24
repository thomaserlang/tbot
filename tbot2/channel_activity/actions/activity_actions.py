from uuid import UUID

import sqlalchemy as sa

from tbot2.common.schemas.pub_sub_event import PubSubEvent
from tbot2.contexts import AsyncSession, get_session
from tbot2.database import conn

from ..models.activity_model import MActivity
from ..schemas.activity_schemas import Activity, ActivityCreate, ActivityUpdate
from ..types.activity_types import ActivityId


async def get_activity(
    *,
    activity_id: ActivityId | None = None,
    provider_message_id: str | None = None,
    session: AsyncSession | None = None,
) -> Activity | None:
    async with get_session(session) as session:
        stmt = sa.select(MActivity)
        if activity_id:
            stmt = stmt.where(MActivity.id == activity_id)
        if provider_message_id:
            stmt = stmt.where(MActivity.provider_message_id == provider_message_id)
        result = await session.scalar(stmt)
        if result:
            return Activity.model_validate(result)
        return None


async def create_activity(
    *,
    data: ActivityCreate,
    publish: bool = True,
    session: AsyncSession | None = None,
) -> Activity:
    async with get_session(session) as session:
        data_ = data.model_dump()
        await session.execute(sa.insert(MActivity).values(data_))

    activity = Activity.model_validate(data)
    if publish:
        await publish_activity(
            channel_id=data.channel_id,
            event=PubSubEvent[Activity](type='activity', action='new', data=activity),
        )
    return activity


async def update_activity(
    *,
    activity_id: ActivityId,
    data: ActivityUpdate,
    publish: bool = True,
    session: AsyncSession | None = None,
) -> Activity:
    async with get_session(session) as session:
        data_ = data.model_dump(exclude_unset=True)

        await session.execute(
            sa.update(MActivity).where(MActivity.id == activity_id).values(data_)
        )
        activity = await get_activity(
            activity_id=activity_id,
            session=session,
        )
        if not activity:
            raise Exception('Activity not updated')
    if publish:
        await publish_activity(
            channel_id=activity.channel_id,
            event=PubSubEvent[Activity](
                type='activity',
                action='updated',
                data=activity,
            ),
        )
    return activity


async def delete_activity(
    *,
    activity_id: ActivityId,
    publish: bool = True,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        activity = await get_activity(
            activity_id=activity_id,
            session=session,
        )
        if not activity:
            return False
        await session.execute(sa.delete(MActivity).where(MActivity.id == activity_id))
    if publish:
        await publish_activity(
            channel_id=activity.channel_id,
            event=PubSubEvent[Activity](
                type='activity',
                action='deleted',
                data=activity,
            ),
        )
    return True


def activity_queue_key(channel_id: UUID) -> str:
    return f'tbot:channel-activity:{channel_id}'


async def publish_activity(
    channel_id: UUID,
    event: PubSubEvent[Activity],
) -> None:
    await conn.redis.publish(  # type: ignore
        activity_queue_key(channel_id=channel_id),
        event.model_dump_json(),
    )
