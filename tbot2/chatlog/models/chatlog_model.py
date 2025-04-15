import sys
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.common import Provider
from tbot2.model_base import Base


class MChatlog(Base):
    __tablename__ = 'chatlogs'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID(), primary_key=True)
    type: Mapped[str] = mapped_column(sa.String(255))
    sub_type: Mapped[str | None] = mapped_column(sa.String(255), nullable=True)
    created_at: Mapped[sa.DateTime] = mapped_column(sa.DateTime, nullable=False)
    channel_id: Mapped[UUID] = mapped_column(sa.UUID)
    chatter_id: Mapped[str] = mapped_column(sa.String(255))
    chatter_name: Mapped[str] = mapped_column(sa.String(200))
    chatter_display_name: Mapped[str] = mapped_column(sa.String(200))
    chatter_color: Mapped[str | None] = mapped_column(sa.String(7), nullable=True)
    message: Mapped[str] = mapped_column(sa.String(600))
    msg_id: Mapped[str] = mapped_column(sa.String(255))
    provider: Mapped[Provider] = mapped_column(sa.String(255))
    provider_id: Mapped[str] = mapped_column(sa.String(255))
    twitch_fragments: Mapped[dict[str, str | int | None] | None] = mapped_column(
        sa.JSON, nullable=True
    )
    twitch_badges: Mapped[dict[str, str | int | None] | None] = mapped_column(
        sa.JSON, nullable=True
    )
