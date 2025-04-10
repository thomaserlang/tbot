from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from starlette.authentication import BaseUser

from tbot2.config_settings import config

from ..types.access_level_type import TAccessLevel
from ..types.scope_type import TScope


class TokenData(BaseUser, BaseModel):
    user_id: UUID
    scopes: list[str | TScope]

    @property
    def is_authenticated(self) -> bool:
        return True

    async def channel_has_access(
        self, *, channel_id: UUID, access_level: TAccessLevel
    ) -> bool:
        from tbot2.channel import get_channel_user_access_level

        level = await get_channel_user_access_level(
            user_id=self.user_id,
            channel_id=channel_id,
        )
        if level is None or level.access_level < access_level.value:
            raise HTTPException(
                status_code=403,
                detail='Insufficient access level',
            )
        return True

    def has_any_scope(self, scopes: list[TScope]) -> bool:
        return any(scope in self.scopes for scope in scopes)

    async def is_global_admin(self) -> bool:
        return self.user_id in config.global_admin_user_ids
