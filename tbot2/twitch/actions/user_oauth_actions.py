from dataclasses import dataclass

import sqlalchemy as sa

from tbot2.contexts import get_session

from ..models.twitch_channel import MTwitchChannel


@dataclass(slots=True)
class TwitchOAuthToken:
    access_token: str
    refresh_token: str


async def get_twitch_oauth_token(broadcaster_id: str):
    async with get_session() as session:
        result = await session.scalar(
            sa.select(MTwitchChannel).where(MTwitchChannel.channel_id == broadcaster_id)
        )
        if result is None:
            raise ValueError(f'Channel {broadcaster_id} not found')
        return TwitchOAuthToken(
            access_token=result.twitch_token, refresh_token=result.twitch_refresh_token
        )


async def save_twitch_oauth_token(
    broadcaster_id: str, access_token: str, refresh_token: str
):
    async with get_session() as session:
        await session.execute(
            sa.update(MTwitchChannel)
            .where(MTwitchChannel.channel_id == broadcaster_id)
            .values(
                twitch_token=access_token,
                twitch_refresh_token=refresh_token,
            )
        )
