import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import Base


class MSpotifyOAuth(Base):
    __tablename__ = 'spotify_oauth'
    __table_args__ = {'extend_existing': True if 'pytest' in sys.modules else False}

    channel_id: Mapped[UUID] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('channels.id', ondelete='cascade', onupdate='cascade'),
        primary_key=True,
    )
    access_token: Mapped[str] = mapped_column(sa.String(500))
    refresh_token: Mapped[str] = mapped_column(sa.String(500))
    expires_at: Mapped[datetime] = mapped_column(sa.DateTime(), nullable=True)
    name: Mapped[str] = mapped_column(sa.String(500))
