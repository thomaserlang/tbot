from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class ChannelStreamViewerWatchtime(BaseModel):
    channel_id: UUID
    provider: str
    stream_id: str
    viewer_id: str
    watchtime: int

    model_config = ConfigDict(from_attributes=True)


class ChannelStreamViewerWatchtimeCreate(BaseModel):
    channel_id: UUID
    provider: str
    stream_id: str
    viewer_id: str
    watchtime: int

    @field_validator("provider", "stream_id", "viewer_id", "watchtime")
    def check_not_none(cls, value):
        if value is None:
            raise ValueError("Must not be None")
        return value


class ChannelStreamViewerWatchtimeUpdate(BaseModel):
    watchtime: int | None = None

    @field_validator("watchtime")
    def check_not_none(cls, value):
        if value is None:
            raise ValueError("Must not be None")
        return value
