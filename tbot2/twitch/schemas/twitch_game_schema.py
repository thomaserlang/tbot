from tbot2.common import BaseSchema


class Game(BaseSchema):
    box_art_url: str
    id: str
    name: str
    igdb_id: str


class SearchCategoryResult(BaseSchema):
    id: str
    name: str
    box_art_url: str
