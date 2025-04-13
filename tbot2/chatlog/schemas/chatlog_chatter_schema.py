from tbot2.common import BaseRequestSchema


class ChatterRequest(BaseRequestSchema):
    chatter_id: str
    chatter_name: str
    chatter_display_name: str
