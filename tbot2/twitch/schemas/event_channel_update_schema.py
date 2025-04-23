
from pydantic import BaseModel


class EventChannelUpdate(BaseModel):
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    title: str
    language: str | None
    category_id: str | None
    category_name: str | None
    content_classification_labels: list[str] | None
