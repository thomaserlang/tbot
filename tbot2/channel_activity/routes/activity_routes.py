from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Query, Security

from tbot2.channel_activity import get_activity
from tbot2.channel_activity.actions.activity_actions import (
    delete_activity,
    update_activity,
)
from tbot2.common import ErrorMessage, TAccessLevel, TokenData
from tbot2.common.utils.split_list_util import split_list
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQueryDep, page_cursor

from ..models.activity_model import MActivity
from ..schemas.activity_schemas import Activity, ActivityUpdate
from ..types.activity_type import ActivityId, ActivityScope, ActivityType

router = APIRouter()


@router.get('/channels/{channel_id}/activities', name='Get Activities')
async def get_activities_route(
    channel_id: UUID,
    page_query: PageCursorQueryDep,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ActivityScope.READ])
    ],
    type: Annotated[list[ActivityType | str] | None, Query()] = None,
    not_type: Annotated[list[ActivityType | str] | None, Query()] = None,
    min_count: Annotated[
        list[str] | None, Query(description='<type>.<min count>')
    ] = None,
) -> PageCursor[Activity]:
    await token_data.channel_require_access(
        channel_id=channel_id, access_level=TAccessLevel.MOD
    )
    stmt = (
        sa.select(MActivity)
        .where(
            MActivity.channel_id == channel_id,
        )
        .order_by(MActivity.id.desc())
    )

    if type:
        stmt = stmt.where(MActivity.type.in_(type))
    if not_type:
        stmt = stmt.where(~MActivity.type.in_(not_type))

    if min_count:
        min_count_dict = min_count_query_to_dict(min_count)
        keys = [
            k
            for k in min_count_dict.keys()
            if (not not_type or k not in not_type) and (not type or k not in type)
        ]
        stmt = stmt.where(
            sa.or_(
                *[
                    sa.and_(MActivity.type == type_str, MActivity.count >= count)
                    for type_str, count in min_count_dict.items()
                ],
                sa.and_(MActivity.type.notin_(keys)),
            )
        )

    return await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=Activity,
        count_total=False,
    )


def min_count_query_to_dict(
    min_count: list[str] | None,
) -> dict[ActivityType | str, int]:
    if not min_count:
        return {}
    result: dict[ActivityType | str, int] = {}
    for item in split_list(min_count):
        try:
            type_str, count_str = item.split('.')
            count = int(count_str)
            result[type_str] = count
        except ValueError as e:
            raise ErrorMessage(
                code=400,
                message=f'Invalid min_count format: {item}',
                type='invalid_request',
            ) from e
    return result


@router.get(
    '/channels/{channel_id}/activities/{activity_id}',
    name='Get Activity',
)
async def get_activity_route(
    channel_id: UUID,
    activity_id: ActivityId,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ActivityScope.READ])
    ],
) -> Activity:
    await token_data.channel_require_access(
        channel_id=channel_id, access_level=TAccessLevel.MOD
    )
    activity = await get_activity(activity_id=activity_id)
    if not activity or activity.channel_id != channel_id:
        raise ErrorMessage(
            code=404,
            message='Activity not found',
            type='not_found',
        )
    return activity


@router.put(
    '/channels/{channel_id}/activities/{activity_id}',
    name='Update Activity',
)
async def update_activity_route(
    channel_id: UUID,
    activity_id: ActivityId,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ActivityScope.READ])
    ],
    data: ActivityUpdate,
) -> Activity:
    await token_data.channel_require_access(
        channel_id=channel_id, access_level=TAccessLevel.MOD
    )
    activity = await get_activity(activity_id=activity_id)
    if not activity or activity.channel_id != channel_id:
        raise ErrorMessage(
            code=404,
            message='Activity not found',
            type='not_found',
        )
    return await update_activity(activity_id=activity_id, data=data)


@router.delete(
    '/channels/{channel_id}/activities/{activity_id}',
    name='Delete Activity',
    status_code=204,
)
async def delete_activity_route(
    channel_id: UUID,
    activity_id: ActivityId,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ActivityScope.READ])
    ],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id, access_level=TAccessLevel.ADMIN
    )
    activity = await get_activity(activity_id=activity_id)
    if not activity or activity.channel_id != channel_id:
        raise ErrorMessage(
            code=404,
            message='Activity not found',
            type='not_found',
        )
    await delete_activity(activity_id=activity_id)
