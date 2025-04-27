from typing import Any, Generic, TypeVar

from tbot2.common import BaseSchema


class SpotifyBaseModel(BaseSchema): ...


class SpotifyExternalUrls(SpotifyBaseModel):
    spotify: str


class SpotifyRestrictions(SpotifyBaseModel):
    reason: str


class SpotifyImage(SpotifyBaseModel):
    url: str
    height: int
    width: int


class SpotifyArtist(SpotifyBaseModel):
    external_urls: SpotifyExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str


class SpotifyAlbum(SpotifyBaseModel):
    album_type: str
    total_tracks: int
    available_markets: list[str]
    external_urls: SpotifyExternalUrls
    href: str
    id: str
    images: list[SpotifyImage]
    name: str
    release_date: str
    release_date_precision: str
    restrictions: SpotifyRestrictions | None = None
    type: str
    uri: str
    artists: list[SpotifyArtist]


class SpotifyExternalIds(SpotifyBaseModel):
    isrc: str | None = None
    ean: str | None = None
    upc: str | None = None


class SpotifyItem(SpotifyBaseModel):
    album: SpotifyAlbum
    artists: list[SpotifyArtist]
    available_markets: list[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: SpotifyExternalIds
    external_urls: SpotifyExternalUrls
    href: str
    id: str
    linked_from: dict[str, Any] | None = None
    restrictions: SpotifyRestrictions | None = None
    name: str
    popularity: int
    preview_url: str | None = None
    track_number: int
    type: str
    uri: str
    is_local: bool


class SpotifyDevice(SpotifyBaseModel):
    id: str | None = None
    is_active: bool
    is_private_session: bool
    is_restricted: bool
    name: str
    type: str
    volume_percent: int


class SpotifyContext(SpotifyBaseModel):
    type: str | None = None
    href: str | None = None
    external_urls: SpotifyExternalUrls | None = None
    uri: str | None = None


class SpotifyActions(SpotifyBaseModel):
    interrupting_playback: bool | None = None
    pausing: bool | None = None
    resuming: bool | None = None
    seeking: bool | None = None
    skipping_next: bool | None = None
    skipping_prev: bool | None = None
    toggling_repeat_context: bool | None = None
    toggling_shuffle: bool | None = None
    toggling_repeat_track: bool | None = None
    transferring_playback: bool | None = None


class SpotifyCurrentlyPlaying(SpotifyBaseModel):
    device: SpotifyDevice | None = None
    context: SpotifyContext | None = None
    timestamp: int
    progress_ms: int | None = None
    is_playing: bool
    item: SpotifyItem | None = None
    currently_playing_type: str
    actions: SpotifyActions


class SpotifyPlayHistory(SpotifyBaseModel):
    track: SpotifyItem
    played_at: str
    context: SpotifyContext | None = None


class SpotifyCursor(SpotifyBaseModel):
    after: str


class SpotifyCursorPaging(SpotifyBaseModel):
    cursors: SpotifyCursor
    href: str
    items: list[SpotifyPlayHistory]
    limit: int
    next: str | None = None


class SpotifyUser(SpotifyBaseModel):
    display_name: str | None = None
    external_urls: SpotifyExternalUrls
    href: str
    id: str
    type: str
    uri: str


T = TypeVar('T')


class SpotifyPaging(SpotifyBaseModel, Generic[T]):
    href: str
    items: list[T]
    limit: int
    next: str | None = None
    offset: int
    previous: str | None = None
    total: int


class SpotifyPlaylistTrack(SpotifyBaseModel):
    added_at: str
    added_by: SpotifyUser
    is_local: bool
    track: SpotifyItem


class SpotifyPlaylist(SpotifyBaseModel):
    collaborative: bool
    description: str | None = None
    external_urls: SpotifyExternalUrls
    href: str
    id: str
    images: list[SpotifyImage]
    name: str
    owner: SpotifyUser
    public: bool | None = None
    snapshot_id: str
    tracks: SpotifyPaging[SpotifyPlaylistTrack]
    type: str
    uri: str
