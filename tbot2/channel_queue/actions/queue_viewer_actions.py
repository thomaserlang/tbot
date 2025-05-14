from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import uuid7

from tbot2.common import ErrorMessage, datetime_now
from tbot2.contexts import get_session

from ..models.channel_queue_viewer_model import MChannelQueueViewer
from ..schemas.queue_viewer_schema import (
    QueueViewer,
    QueueViewerCreate,
)
from .queue_publish_actions import (
    publish_queue_cleared,
    publish_queue_viewer_created,
    publish_queue_viewer_deleted,
)


async def get_queue_viewer(
    channel_queue_viewer_id: UUID,
    session: AsyncSession | None = None,
) -> QueueViewer | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelQueueViewer).where(
                MChannelQueueViewer.id == channel_queue_viewer_id
            )
        )
        if result:
            return QueueViewer.model_validate(result)
        return None


async def get_queue_viewer_by_provider(
    channel_queue_id: UUID,
    provider: str,
    provider_viewer_id: str,
    session: AsyncSession | None = None,
) -> QueueViewer | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelQueueViewer).where(
                MChannelQueueViewer.channel_queue_id == channel_queue_id,
                MChannelQueueViewer.provider == provider,
                MChannelQueueViewer.provider_viewer_id == provider_viewer_id,
            )
        )
        if result:
            return QueueViewer.model_validate(result)
        return None


async def create_queue_viewer(
    channel_queue_id: UUID,
    data: QueueViewerCreate,
    channel_queue_viewer_id: UUID | None = None,
    position: int | None = None,
    session: AsyncSession | None = None,
) -> QueueViewer:
    async with get_session(session) as session:
        id = channel_queue_viewer_id or uuid7()
        data_ = data.model_dump()
        if position is None:
            pos = await session.scalar(
                sa.select(
                    sa.func.coalesce(sa.func.max(MChannelQueueViewer.position), 0) + 1,
                )
                .where(
                    MChannelQueueViewer.channel_queue_id == channel_queue_id,
                )
                .with_for_update()
            )
            if pos is None:
                raise ValueError('Queue not found')
        else:
            pos = position
            await _update_position(
                channel_queue_id=channel_queue_id,
                from_pos=pos,
                inc_pos=10000,
                session=session,
            )

        try:
            await session.execute(
                sa.insert(MChannelQueueViewer.__table__).values(  # type: ignore
                    id=id,
                    channel_queue_id=channel_queue_id,
                    position=pos,
                    created_at=datetime_now(),
                    **data_,
                )
            )
        except sa.exc.IntegrityError as e:
            if 'ix_channel_queue_id_position' in str(e):
                raise ErrorMessage(
                    'Position already taken',
                    type='position_already_taken',
                    code=409,
                ) from e
            raise ErrorMessage(
                'Viewer already in queue',
                type='viewer_already_in_queue',
                code=409,
            ) from e

        if position is not None:
            await _update_position(
                channel_queue_id=channel_queue_id,
                from_pos=10000,
                inc_pos=-9999,
                session=session,
            )

        viewer = await get_queue_viewer(
            channel_queue_viewer_id=id,
            session=session,
        )
        if viewer is None:
            raise ValueError('User not found after creation')
        await publish_queue_viewer_created(
            channel_queue_viewer=viewer,
        )
        return viewer


async def _update_position(
    channel_queue_id: UUID,
    from_pos: int,
    inc_pos: int,
    session: AsyncSession,
) -> None:
    await session.execute(
        sa.update(MChannelQueueViewer.__table__)  # type: ignore
        .where(
            MChannelQueueViewer.channel_queue_id == channel_queue_id,
            MChannelQueueViewer.position >= from_pos,
        )
        .values(position=MChannelQueueViewer.position + inc_pos)
    )


async def delete_queue_viewer(
    channel_queue_viewer_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        viewer = await get_queue_viewer(
            channel_queue_viewer_id=channel_queue_viewer_id,
            session=session,
        )
        if not viewer:
            return False
        result = await session.execute(
            sa.delete(MChannelQueueViewer.__table__).where(  # type: ignore
                MChannelQueueViewer.id == channel_queue_viewer_id,
            )
        )
        if result.rowcount == 0:
            return False
        await _update_position(
            channel_queue_id=viewer.channel_queue_id,
            from_pos=viewer.position,
            inc_pos=-1,
            session=session,
        )
        await publish_queue_viewer_deleted(
            channel_queue_viewer=viewer,
        )
        return True


async def clear_viewer_queue(
    channel_queue_id: UUID, session: AsyncSession | None = None
) -> bool:
    async with get_session(session) as session:
        await session.execute(
            sa.delete(MChannelQueueViewer.__table__).where(  # type: ignore
                MChannelQueueViewer.channel_queue_id == channel_queue_id
            )
        )
        await publish_queue_cleared(channel_queue_id=channel_queue_id)
        return True


async def move_viewer_to_top(
    channel_queue_viewer_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        user = await get_queue_viewer(
            channel_queue_viewer_id=channel_queue_viewer_id,
            session=session,
        )
        if not user:
            return False
        await delete_queue_viewer(
            channel_queue_viewer_id=user.id,
            session=session,
        )
        await create_queue_viewer(
            channel_queue_id=user.channel_queue_id,
            data=QueueViewerCreate(
                provider=user.provider,
                provider_viewer_id=user.provider_viewer_id,
                display_name=user.display_name,
            ),
            channel_queue_viewer_id=user.id,
            position=1,
            session=session,
        )
        return True
