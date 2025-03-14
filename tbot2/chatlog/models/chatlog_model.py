from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import Base


class MChatlog(Base):
    __tablename__ = 'chatlogs'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(sa.String(100))
    sub_type: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    created_at: Mapped[sa.DateTime] = mapped_column(DATETIME(fsp=6, timezone=True))
    channel_id: Mapped[UUID] = mapped_column(sa.UUID)
    chatter_id: Mapped[str] = mapped_column(sa.String(36))
    chatter_name: Mapped[str] = mapped_column(sa.String(200))
    chatter_display_name: Mapped[str] = mapped_column(sa.String(200))
    chatter_color: Mapped[str | None] = mapped_column(sa.String(7), nullable=True)
    message: Mapped[str] = mapped_column(sa.String(600))
    msg_id: Mapped[str] = mapped_column(sa.String(36))
    provider: Mapped[str] = mapped_column(sa.String(100))
    provider_id: Mapped[str] = mapped_column(sa.String(36))
    twitch_fragments: Mapped[dict[str, str | int | None] | None] = mapped_column(
        sa.JSON, nullable=True
    )
    twitch_badges: Mapped[dict[str, str | int | None] | None] = mapped_column(
        sa.JSON, nullable=True
    )
