import sqlalchemy as sa

from tbot2.channel_viewer import ViewerNameHistoryRequest, save_viewers_name_history
from tbot2.common import ChatMessage
from tbot2.contexts import AsyncSession, get_session

from ..models.chatlog_model import MChatlog


async def create_chatlog(
    data: ChatMessage,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        await session.execute(
            sa.insert(MChatlog.__table__).values(  # type: ignore
                **data.model_dump(),
            )
        )

        await save_viewers_name_history(
            provider=data.provider,
            viewers=[
                ViewerNameHistoryRequest(
                    provider_viewer_id=data.provider_viewer_id,
                    name=data.viewer_name,
                    display_name=data.viewer_display_name,
                )
            ],
            session=session,
        )

    return True
