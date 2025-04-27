
from tbot2.common import BaseRequestSchema, BaseSchema, Provider


class ViewerNameHistoryRequest(BaseRequestSchema):
    provider_viewer_id: str
    name: str
    display_name: str


class ViewerName(BaseSchema):
    provider: Provider
    provider_viewer_id: str
    name: str
    display_name: str


