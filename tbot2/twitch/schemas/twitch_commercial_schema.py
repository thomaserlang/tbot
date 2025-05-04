from tbot2.common import BaseSchema


class RunCommercialResponse(BaseSchema):
    length: int
    "The length of the commercial you requested. If you request a commercial that's longer than 180 seconds, the API uses 180 seconds."  # noqa: E501
    message: str
    'A message that indicates whether Twitch was able to serve an ad.'
    retry_after: int
    'The number of seconds you must wait before you can run another commercial.'
