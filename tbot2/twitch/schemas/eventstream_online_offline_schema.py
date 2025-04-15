from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class EventStreamOnline(BaseModel):
    id: str
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    type: str | Literal['live']
    started_at: datetime


class EventStreamOffline(BaseModel):
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
