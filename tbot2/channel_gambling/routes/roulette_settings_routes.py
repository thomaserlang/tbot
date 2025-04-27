from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Security

from tbot2.channel_points import ChannelPointSettingScope
from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated

from ..actions.roulette_settings_actions import (
    get_roulette_settings,
    update_roulette_settings,
)
from ..schemas.roulette_settings_schema import (
    RouletteSettings,
    RouletteSettingsUpdate,
)

router = APIRouter()


@router.get(
    '/channels/{channel_id}/roulette-settings',
    name='Get Roulette Settings',
)
async def get_roulette_settings_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelPointSettingScope.READ])
    ],
) -> RouletteSettings:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    settings = await get_roulette_settings(
        channel_id=channel_id,
    )
    return settings


@router.put(
    '/channels/{channel_id}/roulette-settings',
    name='Update Roulette Settings',
)
async def update_roulette_settings_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelPointSettingScope.WRITE])
    ],
    data: RouletteSettingsUpdate,
) -> RouletteSettings:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    settings = await update_roulette_settings(
        channel_id=channel_id,
        data=data,
    )
    return settings
