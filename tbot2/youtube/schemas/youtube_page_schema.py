from typing import Annotated, Generic, TypeVar

from pydantic import Field

from tbot2.common import BaseSchema

T = TypeVar('T')


class YoutubePageInfo(BaseSchema):
    total_results: Annotated[int, Field(alias='totalResults')]
    results_per_page: Annotated[int, Field(alias='resultsPerPage')]


class YoutubePage(BaseSchema, Generic[T]):
    items: list[T]
    page_info: Annotated[YoutubePageInfo, Field(alias='pageInfo')]
    next_page_token: Annotated[str | None, Field(alias='nextPageToken')] = None
