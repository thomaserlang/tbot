from uuid import UUID

from pydantic import BaseModel
from starlette.authentication import BaseUser

from ..types.access_level_type import TAccessLevel
from ..types.scope_type import TScope


class TokenData(BaseUser, BaseModel):
    user_id: UUID
    scopes: list[str | TScope]

    @property
    def is_authenticated(self) -> bool:
        return True

    async def is_valid_for_channel(
        self, *, channel_id: UUID, access_level: TAccessLevel
    ) -> bool:
        return True

    def has_any_scope(self, scopes: list[TScope]) -> bool:
        return any(scope in self.scopes for scope in scopes)
