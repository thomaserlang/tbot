from collections.abc import Awaitable
from typing import cast
from uuid import UUID

from tbot2.common import MentionPartRequest
from tbot2.database import conn

from ..actions.activity_actions import update_activity
from ..schemas.activity_schemas import ActivityId, ActivityUpdate

"""
Used e.g. for Twitch since they send each gifted recipient as a separate event
"""


async def start_collect_gift_recipients(
    activity_id: ActivityId, gift_id: str, total: int
) -> None:
    async with conn.redis.pipeline() as pipe:
        await pipe.set(total_key(gift_id), total, ex=300)
        await pipe.set(activity_id_key(gift_id), str(activity_id), ex=300)
        await pipe.execute()


async def add_gift_recipient(gift_id: str, recipient: MentionPartRequest) -> None:
    r = await cast(
        Awaitable[int],
        conn.redis.rpush(
            recipients_list_key(gift_id),
            recipient.model_dump_json(),
        ),
    )
    if r == 1:
        await conn.redis.expire(recipients_list_key(gift_id), 300)

    count = await cast(Awaitable[int], conn.redis.llen(recipients_list_key(gift_id)))
    total = int(await cast(Awaitable[str], conn.redis.get(total_key(gift_id))))

    if count == total:
        activity_id = await cast(
            Awaitable[str],
            conn.redis.get(
                activity_id_key(gift_id),
            ),
        )
        recipients = await cast(
            Awaitable[list[str]],
            conn.redis.lrange(recipients_list_key(gift_id), 0, -1),  # type: ignore
        )
        from loguru import logger

        logger.info(recipients)
        await update_activity(
            activity_id=ActivityId(UUID(activity_id)),
            data=ActivityUpdate(
                gifted_viewers=[
                    MentionPartRequest.model_validate_json(recipient)
                    for recipient in recipients
                ],
            ),
        )

        async with conn.redis.pipeline() as pipe:
            await pipe.delete(recipients_list_key(gift_id))
            await pipe.delete(total_key(gift_id))
            await pipe.delete(
                activity_id_key(gift_id),
            )
            await pipe.execute()


def total_key(gift_id: str) -> str:
    return f'tbot2:activity:gift:total:{gift_id}'


def recipients_list_key(gift_id: str) -> str:
    return f'tbot2:activity:gift:recipients:{gift_id}'


def activity_id_key(gift_id: str) -> str:
    return f'tbot2:activity:gift:activity_id:{gift_id}'
