import sys
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.common import Provider
from tbot2.common.utils.sqlalchemy_utils import UtcDateTime
from tbot2.model_base import Base


class MProviderViewerNameHistory(Base):
    __tablename__ = 'provider_viewer_name_history'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    provider: Mapped[Provider] = mapped_column(sa.String(255), primary_key=True)
    provider_viewer_id: Mapped[str] = mapped_column(sa.String(255), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(200), primary_key=True)
    display_name: Mapped[str] = mapped_column(sa.String(200))
    last_seen_at: Mapped[datetime] = mapped_column(UtcDateTime)
