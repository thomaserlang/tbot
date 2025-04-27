from datetime import timedelta
from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.common import datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..actions.channel_user_access_level_actions import (
    set_channel_user_access_level,
)
from ..models.channel_user_invite_model import MChannelUserInvite
from ..schemas.channel_user_invite_schema import (
    ChannelUserInvite,
    ChannelUserInviteCreate,
    ChannelUserInviteUpdate,
)


async def get_channel_user_invite(
    *,
    channel_user_invite_id: UUID,
    session: AsyncSession | None = None,
) -> ChannelUserInvite | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelUserInvite).where(
                MChannelUserInvite.id == channel_user_invite_id
            )
        )
        if result:
            return ChannelUserInvite.model_validate(result)


async def create_channel_user_invite(
    channel_id: UUID,
    data: ChannelUserInviteCreate,
    session: AsyncSession | None = None,
) -> ChannelUserInvite:
    async with get_session(session) as session:
        id = uuid7()
        await session.execute(
            sa.insert(MChannelUserInvite).values(
                id=id,
                channel_id=channel_id,
                access_level=data.access_level.value,
                created_at=datetime_now(),
                expires_at=datetime_now() + timedelta(hours=24),
            )
        )
        invite = await get_channel_user_invite(
            channel_user_invite_id=id, session=session
        )
        if not invite:
            raise Exception(
                f'Failed to create channel user invite for channel {channel_id}'
            )
        return invite


async def update_channel_user_invite(
    *,
    channel_user_invite_id: UUID,
    data: ChannelUserInviteUpdate,
    session: AsyncSession | None = None,
) -> ChannelUserInvite:
    async with get_session(session) as session:
        channel_user_invite = await get_channel_user_invite(
            channel_user_invite_id=channel_user_invite_id, session=session
        )
        if not channel_user_invite:
            raise Exception(f'Channel user invite {channel_user_invite_id} not found')

        await session.execute(
            sa.update(MChannelUserInvite)
            .where(MChannelUserInvite.id == channel_user_invite_id)
            .values(
                access_level=data.access_level.value,
                expires_at=datetime_now() + timedelta(hours=24),
            )
        )
        invite = await get_channel_user_invite(
            channel_user_invite_id=channel_user_invite_id, session=session
        )
        if not invite:
            raise Exception(
                f'Failed to update channel user invite {channel_user_invite_id}'
            )
        return invite


async def delete_channel_user_invite(
    *,
    channel_user_invite_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        r = await session.execute(
            sa.delete(MChannelUserInvite).where(
                MChannelUserInvite.id == channel_user_invite_id
            )
        )
        return r.rowcount > 0


async def channel_user_invite_accept(
    *,
    channel_user_invite_id: UUID,
    user_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        channel_user_invite = await get_channel_user_invite(
            channel_user_invite_id=channel_user_invite_id, session=session
        )
        if not channel_user_invite:
            raise Exception(f'Channel user invite {channel_user_invite_id} not found')

        if not await delete_channel_user_invite(
            channel_user_invite_id=channel_user_invite_id, session=session
        ):
            raise Exception('Invite was already claimed')

        await set_channel_user_access_level(
            channel_id=channel_user_invite.channel_id,
            user_id=user_id,
            access_level=channel_user_invite.access_level,
            session=session,
        )

        return True
