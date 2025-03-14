import sys

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import Base


class MTwitchChannel(Base):
    __tablename__ = 'twitch_channels'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    channel_id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(25))
    twitch_token: Mapped[str] = mapped_column(sa.String(200))
    twitch_refresh_token: Mapped[str] = mapped_column(sa.String(200))
    twitch_scope: Mapped[list[str]] = mapped_column(sa.JSON)
