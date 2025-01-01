import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import ModelBase


class MChannel(ModelBase):
    __tablename__ = 'channels'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    display_name: Mapped[str] = mapped_column(sa.String(200))
    twitch_id: Mapped[str | None] = mapped_column(sa.String(36))
    created_at: Mapped[datetime]
    bot_active: Mapped[bool]
    bot_muted: Mapped[bool]
    bot_chatlog_enabled: Mapped[bool]
