from typing import Any

import sqlalchemy as sa
from humanize import intcomma

from tbot2.channel_points import MChatterPoints
from tbot2.common import ChatMessage
from tbot2.contexts import get_session
from tbot2.twitch import lookup_twitch_users

from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(
    provider='twitch',
    vars=('points_ranking',),
)
async def points_ranking_vars(
    chat_message: ChatMessage, command: TCommand, vars: MessageVars
) -> None:
    async with get_session() as session:
        result = await session.execute(
            sa.select(
                MChatterPoints.provider_viewer_id,
                MChatterPoints.points,
                sa.func.rank()
                .over(
                    order_by=MChatterPoints.points.desc(),
                    partition_by=MChatterPoints.channel_id,
                )
                .label('rank'),
            ).where(
                MChatterPoints.channel_id == chat_message.channel_id,
                MChatterPoints.provider == chat_message.provider,
            )
        )
        ranks: list[dict[str, Any]] = []
        for row in result:
            ranks.append(
                {
                    'provider_viewer_id': row[0],
                    'points': row[1],
                    'rank': row[2],
                }
            )

        users = await lookup_twitch_users(
            channel_id=chat_message.channel_id,
            user_ids=[r['provider_viewer_id'] for r in ranks],
        )

        for rank, user in zip(ranks, users, strict=True):
            rank['user'] = user.display_name if user else 'Unknown'

        vars['points_ranking'].value = ', '.join(
            f'{r["rank"]}. {r["user"]} ({intcomma(r["points"])})' for r in ranks
        )
