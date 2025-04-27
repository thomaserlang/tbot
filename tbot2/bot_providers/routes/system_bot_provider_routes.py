from typing import Annotated

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, Security

from tbot2.bot_providers import (
    BotProviderPublic,
    MBotProvider,
    delete_bot_provider,
    get_system_bot_provider,
)
from tbot2.common import Provider, TokenData
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQuery, page_cursor

router = APIRouter()


@router.get('/system-bot-providers', name='Get System Bot Providers')
async def get_system_bot_providers_route(
    page_query: Annotated[PageCursorQuery, Depends()],
    token_data: Annotated[TokenData, Security(authenticated)],
) -> PageCursor[BotProviderPublic]:
    if not await token_data.is_global_admin():
        raise HTTPException(
            status_code=403,
            detail='Not enough permissions',
        )

    stmt = (
        sa.select(
            MBotProvider,
        )
        .where(MBotProvider.system_default.is_(True))
        .order_by(MBotProvider.id.desc())
    )

    return await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=BotProviderPublic,
    )


@router.delete(
    '/system-bot-providers/{provider}',
    name='Delete System Bot Provider',
    status_code=204,
)
async def delete_system_bot_provider_route(
    provider: Provider,
    token_data: Annotated[TokenData, Security(authenticated)],
) -> None:
    if not await token_data.is_global_admin():
        raise HTTPException(
            status_code=403,
            detail='Not enough permissions',
        )
    p = await get_system_bot_provider(
        provider=provider,
    )
    if not p:
        raise HTTPException(
            status_code=404,
            detail='System bot provider not found',
        )
    await delete_bot_provider(
        bot_provider_id=p.id,
        session=None,
    )


@router.get(
    '/system-bot-providers/{provider}',
    name='Get System Bot Provider',
)
async def get_system_bot_provider_route(
    provider: Provider,
    token_data: Annotated[TokenData, Security(authenticated)],
) -> BotProviderPublic:
    if not await token_data.is_global_admin():
        raise HTTPException(
            status_code=403,
            detail='Not enough permissions',
        )
    p = await get_system_bot_provider(
        provider=provider,
    )
    if not p:
        raise HTTPException(
            status_code=404,
            detail='System bot provider not found',
        )
    return BotProviderPublic.model_validate(p)
