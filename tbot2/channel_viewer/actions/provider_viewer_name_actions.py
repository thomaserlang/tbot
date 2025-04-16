import sqlalchemy as sa
from sqlalchemy.dialects.mysql import insert

from tbot2.common import Provider, datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..models.provider_viewer_name_history_model import MProviderViewerNameHistory
from ..schemas.viewer_schemas import ViewerName, ViewerNameHistoryRequest


async def get_viewer_name(
    provider: Provider,
    provider_viewer_id: str,
    session: AsyncSession | None = None,
) -> ViewerName | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MProviderViewerNameHistory)
            .where(
                MProviderViewerNameHistory.provider == provider,
                MProviderViewerNameHistory.provider_viewer_id == provider_viewer_id,
            )
            .order_by(MProviderViewerNameHistory.last_seen_at.desc())
        )
        if result:
            return ViewerName.model_validate(result)


async def save_viewers_name_history(
    provider: Provider,
    viewers: list[ViewerNameHistoryRequest],
    session: AsyncSession | None = None,
) -> None:
    last_seen_at = datetime_now()
    async with get_session(session) as session:
        await session.execute(
            insert(MProviderViewerNameHistory.__table__)  # type: ignore
            .values(
                [
                    {
                        'provider': provider,
                        'provider_viewer_id': viewer.provider_viewer_id,
                        'name': viewer.name,
                        'display_name': viewer.display_name,
                        'last_seen_at': last_seen_at,
                    }
                    for viewer in viewers
                ]
            )
            .on_duplicate_key_update(
                name=sa.func.values(MProviderViewerNameHistory.name),
                display_name=sa.func.values(MProviderViewerNameHistory.display_name),
                last_seen_at=sa.func.values(MProviderViewerNameHistory.last_seen_at),
            )
        )
