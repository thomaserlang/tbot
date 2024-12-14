from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import ModelBase


class MChatlogUsername(ModelBase):
    __tablename__ = 'chatlog_chatters'

    provider: Mapped[str] = mapped_column(sa.String(100))
    chatter_id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    chatter_name: Mapped[str] = mapped_column(sa.String(200))
    chatter_display_name: Mapped[str] = mapped_column(sa.String(200))
    last_seen_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
