from typing import Any

import sqlalchemy as sa
from humanize import intcomma

from tbot2.channel_points import MChatterPoints
from tbot2.common import ChatMessage, TProvider
from tbot2.contexts import get_session
from tbot2.twitch import lookup_twitch_users

from ..types import TCommand, TMessageVars
from ..var_filler import fills_vars


@fills_vars(
    provider=TProvider.twitch,
    vars=('points_ranking',),
)
async def points_ranking_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
) -> None:
    async with get_session() as session:
        result = await session.execute(
            sa.select(
                MChatterPoints.chatter_id,
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
                    'chatter_id': row[0],
                    'points': row[1],
                    'rank': row[2],
                }
            )

        users = await lookup_twitch_users(
            channel_id=chat_message.channel_id,
            user_ids=[r['chatter_id'] for r in ranks],
        )

        for rank, user in zip(ranks, users, strict=True):
            rank['user'] = user.display_name if user else 'Unknown'

        vars['points_ranking'].value = ', '.join(
            f'{r["rank"]}. {r["user"]} ({intcomma(r["points"])})' for r in ranks
        )
