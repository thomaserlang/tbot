import sys
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import Base


class MChannelQuote(Base):
    __tablename__ = 'channel_quotes'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    channel_id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    provider: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    created_by_provider_viewer_id: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    created_by_display_name: Mapped[str] = mapped_column(sa.String(200), nullable=False)
    message: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    number: Mapped[int] = mapped_column(sa.Integer, nullable=False, server_default='1')
    created_at: Mapped[sa.DateTime] = mapped_column(sa.DateTime, nullable=False)
    updated_at: Mapped[sa.DateTime] = mapped_column(sa.DateTime, nullable=True)
