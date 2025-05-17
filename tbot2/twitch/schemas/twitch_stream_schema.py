from datetime import datetime

from tbot2.common import BaseSchema


class TwitchStream(BaseSchema):
    id: str
    'An ID that identifies the stream. You can use this ID later to look up the video on demand (VOD).'  # noqa: E501
    user_id: str
    "The ID of the user that's broadcasting the stream."
    user_login: str
    "The user's login name."
    user_name: str
    "The user's display name."
    game_id: str
    'The ID of the category or game being played.'
    game_name: str
    'The name of the category or game being played.'
    type: str
    'The type of stream. Possible values are: live. If an error occurs, this field is set to an empty string.'  # noqa: E501
    title: str
    "The stream's title. Is an empty string if not set."
    tags: list[str]
    'The tags applied to the stream.'
    viewer_count: int
    'The number of users watching the stream.'
    started_at: datetime
    'The UTC date and time (in RFC3339 format) of when the broadcast began.'
    language: str
    'The language that the stream uses. This is an ISO 639-1 two-letter language code or other if the stream uses a language not in the list of supported stream languages.'  # noqa: E501
    thumbnail_url: str
    'A URL to an image of a frame from the last 5 minutes of the stream. Replace the width and height placeholders in the URL ({width}x{height}) with the size of the image you want, in pixels.'  # noqa: E501
    is_mature: bool
    'A Boolean value that indicates whether the stream is meant for mature audiences.'
