from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Security

from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated

from ..actions.chat_filter_actions import (
    create_chat_filter,
    delete_chat_filter,
    get_chat_filter,
    get_chat_filters,
    update_chat_filter,
)
from ..filters import FilterTypeCreateUnion, FilterTypesUnion, FilterTypeUpdateUnion
from ..types import ChatFilterScope

router = APIRouter()


@router.get(
    '/channels/{channel_id}/chat-filters',
    name='Get channel filters',
    responses={
        200: {
            'model': list[FilterTypesUnion],
        }
    },
)
async def get_chat_filters_route(  # noqa: ANN201
    channel_id: UUID,
    token_data: Annotated[
        TokenData,
        Security(authenticated, scopes=[ChatFilterScope.READ]),
    ],
):
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    filters = await get_chat_filters(
        channel_id=channel_id,
    )
    return filters


@router.get(
    '/channels/{channel_id}/chat-filters/{filter_id}',
    name='Get channel filter',
    responses={
        200: {
            'model': FilterTypesUnion,
        }
    },
)
async def get_chat_filter_route(  # noqa: ANN201
    channel_id: UUID,
    filter_id: UUID,
    token_data: Annotated[
        TokenData,
        Security(authenticated, scopes=[ChatFilterScope.READ]),
    ],
):
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    filter = await get_chat_filter(
        filter_id=filter_id,
    )
    if filter is None or filter.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail=f'Filter with id {filter_id} not found for channel {channel_id}',
        )
    return filter


@router.post(
    '/channels/{channel_id}/chat-filters',
    name='Create channel filter',
    responses={
        201: {
            'model': FilterTypesUnion,
        }
    },
    status_code=201,
)
async def create_chat_filter_route(  # noqa: ANN201
    channel_id: UUID,
    data: FilterTypeCreateUnion,  # type: ignore
    token_data: Annotated[
        TokenData,
        Security(authenticated, scopes=[ChatFilterScope.WRITE]),
    ],
):
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    filter = await create_chat_filter(
        channel_id=channel_id,
        data=data,  # type: ignore
    )

    return filter


@router.put(
    '/channels/{channel_id}/chat-filters/{filter_id}',
    name='Update channel filter',
    responses={
        200: {
            'model': FilterTypesUnion,
        }
    },
)
async def update_chat_filter_route(  # noqa: ANN201
    channel_id: UUID,
    filter_id: UUID,
    data: FilterTypeUpdateUnion,  # type: ignore
    token_data: Annotated[
        TokenData,
        Security(authenticated, scopes=[ChatFilterScope.WRITE]),
    ],
):
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    prev_filter = await get_chat_filter(
        filter_id=filter_id,
    )
    if prev_filter is None or prev_filter.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail=f'Filter with id {filter_id} not found for channel {channel_id}',
        )
    if prev_filter.type != data.type:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail=f'Filter type mismatch: {prev_filter.type} != {data.type}',  # type: ignore
        )

    filter = await update_chat_filter(
        filter_id=filter_id,
        data=data,  # type: ignore
    )
    return filter


@router.delete(
    '/channels/{channel_id}/chat-filters/{filter_id}',
    name='Delete channel filter',
    status_code=204,
)
async def delete_chat_filter_route(
    channel_id: UUID,
    filter_id: UUID,
    token_data: Annotated[
        TokenData,
        Security(authenticated, scopes=[ChatFilterScope.WRITE]),
    ],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    filter = await get_chat_filter(
        filter_id=filter_id,
    )
    if filter is None or filter.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail=f'Filter with id {filter_id} not found for channel {channel_id}',
        )
    await delete_chat_filter(
        filter_id=filter_id,
    )
