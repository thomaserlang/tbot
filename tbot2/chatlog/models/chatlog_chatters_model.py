import sys
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.common import Provider
from tbot2.model_base import Base


class MChatlogChatters(Base):
    __tablename__ = 'chatlog_chatters'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    provider: Mapped[Provider] = mapped_column(sa.String(255), primary_key=True)
    chatter_id: Mapped[str] = mapped_column(sa.String(255), primary_key=True)
    chatter_name: Mapped[str] = mapped_column(sa.String(200), primary_key=True)
    chatter_display_name: Mapped[str] = mapped_column(sa.String(200))
    last_seen_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
