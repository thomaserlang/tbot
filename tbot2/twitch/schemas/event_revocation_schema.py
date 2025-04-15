from pydantic import BaseModel


class EventRevocation(BaseModel):
    id: str
    status: str
    type: str
    condition: dict[str, str]
