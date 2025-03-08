
from uuid import UUID

from pydantic import BaseModel


class TokenData(BaseModel):
    channel_id: UUID