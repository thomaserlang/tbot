from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import Base


class MChatlogUserStats(Base):
    __tablename__ = 'chatlog_chatter_stats'

    channel_id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    chatter_id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    chat_messages: Mapped[int] = mapped_column(sa.Integer)
    bans: Mapped[int] = mapped_column(sa.Integer)
    timeouts: Mapped[int] = mapped_column(sa.Integer)
    deletes: Mapped[int] = mapped_column(sa.Integer)
