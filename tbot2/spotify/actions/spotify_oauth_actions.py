from dataclasses import dataclass
from uuid import UUID

import sqlalchemy as sa

from tbot2.contexts import AsyncSession, get_session
from tbot2.spotify.models.spotify_oauth_model import MSpotifyOAuth


@dataclass(slots=True)
class SpotifyOAuthToken:
    access_token: str
    refresh_token: str


async def get_spotify_oauth_token(
    channel_id: UUID, session: AsyncSession | None = None
):
    async with get_session() as session:
        result = await session.scalar(
            sa.select(MSpotifyOAuth).where(MSpotifyOAuth.channel_id == channel_id)
        )
        if result is None:
            raise ValueError(f'Spotify not connected for channel {channel_id}')
        return SpotifyOAuthToken(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
        )


async def save_spotify_oauth_token(
    channel_id: UUID,
    access_token: str,
    refresh_token: str,
    session: AsyncSession | None = None,
):
    async with get_session(session) as session:
        result = await session.execute(
            sa.update(MSpotifyOAuth)
            .where(MSpotifyOAuth.channel_id == channel_id)
            .values(
                access_token=access_token,
                refresh_token=refresh_token,
            )
        )
        if result.rowcount == 0:
            await session.execute(
                sa.insert(MSpotifyOAuth).values(
                    channel_id=channel_id,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )
            )
