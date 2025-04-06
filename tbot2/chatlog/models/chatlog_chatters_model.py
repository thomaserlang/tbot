from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.common import TProvider
from tbot2.model_base import Base


class MChatlogChatters(Base):
    __tablename__ = 'chatlog_chatters'

    provider: Mapped[TProvider] = mapped_column(sa.String(100), primary_key=True)
    chatter_id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    chatter_name: Mapped[str] = mapped_column(sa.String(200))
    chatter_display_name: Mapped[str] = mapped_column(sa.String(200))
    last_seen_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
