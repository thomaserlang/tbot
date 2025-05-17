from datetime import datetime
from typing import Annotated

from pydantic import Field

from tbot2.common import BaseSchema


class Thumbnail(BaseSchema):
    url: str
    "The image's URL."
    width: int
    "The image's width."
    height: int
    "The image's height."


class LocalizedSnippet(BaseSchema):
    title: str
    'The localized video title.'
    description: str
    'The localized video description.'


class RegionRestriction(BaseSchema):
    allowed: list[str] | None = None
    'A list of region codes that identify countries where the video is viewable.'
    blocked: list[str] | None = None
    'A list of region codes that identify countries where the video is blocked.'


class VideoSnippet(BaseSchema):
    published_at: Annotated[datetime, Field(alias='publishedAt')]
    'The date and time that the video was published.'
    channel_id: Annotated[str, Field(alias='channelId')]
    'The ID that YouTube uses to uniquely identify the channel that the video was uploaded to.'  # noqa: E501
    title: str
    "The video's title."
    description: str
    "The video's description."
    thumbnails: dict[str, Thumbnail]
    'A map of thumbnail images associated with the video.'
    channel_title: Annotated[str, Field(alias='channelTitle')]
    'Channel title for the channel that the video belongs to.'
    tags: list[str] | None = None
    'A list of keyword tags associated with the video.'
    category_id: Annotated[str, Field(alias='categoryId')]
    'The YouTube video category associated with the video.'
    live_broadcast_content: Annotated[str, Field(alias='liveBroadcastContent')]
    'Indicates if the video is an upcoming/active live broadcast.'
    default_language: Annotated[str | None, Field(alias='defaultLanguage')] = None
    "The language of the text in the video resource's snippet.title and snippet.description properties."  # noqa: E501
    localized: LocalizedSnippet
    "Contains either a localized title and description for the video or the title in the default language for the video's metadata."  # noqa: E501
    default_audio_language: Annotated[
        str | None, Field(alias='defaultAudioLanguage')
    ] = None
    "The default_audio_language property specifies the language spoken in the video's default audio track."  # noqa: E501


class ContentDetails(BaseSchema):
    duration: str
    'The length of the video.'
    dimension: str
    'Indicates whether the video is available in 3D or in 2D.'
    definition: str
    'Indicates whether the video is available in high definition (HD) or only in standard definition.'  # noqa: E501
    caption: str
    'Indicates whether captions are available for the video.'
    licensed_content: Annotated[bool, Field(alias='licensedContent')]
    'Indicates whether the video represents licensed content.'
    region_restriction: Annotated[
        RegionRestriction | None, Field(alias='regionRestriction')
    ] = None
    'Contains information about the countries where a video is (or is not) viewable.'
    projection: str
    'Specifies the projection format of the video.'
    has_custom_thumbnail: Annotated[bool | None, Field(alias='hasCustomThumbnail')] = (
        None
    )
    'Indicates whether the video uploader has provided a custom thumbnail image for the video.'  # noqa: E501


class VideoStatus(BaseSchema):
    upload_status: Annotated[str, Field(alias='uploadStatus')]
    'The status of the uploaded video.'
    failure_reason: Annotated[str | None, Field(alias='failureReason')] = None
    'This value explains why a video failed to upload.'
    rejection_reason: Annotated[str | None, Field(alias='rejectionReason')] = None
    'This value explains why YouTube rejected an uploaded video.'
    privacy_status: Annotated[str, Field(alias='privacyStatus')]
    "The video's privacy status."
    publish_at: Annotated[datetime | None, Field(alias='publishAt')] = None
    'The date and time when the video is scheduled to publish.'
    license: str
    "The video's license."
    embeddable: bool
    'This value indicates whether the video can be embedded on another website.'
    public_stats_viewable: Annotated[bool, Field(alias='publicStatsViewable')]
    "This value indicates whether the extended video statistics on the video's watch page are publicly viewable."  # noqa: E501
    made_for_kids: Annotated[bool, Field(alias='madeForKids')]
    'This value indicates whether the video is designated as child-directed.'
    self_declared_made_for_kids: Annotated[bool, Field(alias='selfDeclaredMadeForKids')]
    'This property allows the channel owner to designate the video as being child-directed.'  # noqa: E501
    contains_synthetic_media: Annotated[bool, Field(alias='containsSyntheticMedia')]
    'This property allows the channel owner to disclose that a video contains realistic Altered or Synthetic (A/S) content.'  # noqa: E501


class Statistics(BaseSchema):
    view_count: Annotated[str, Field(alias='viewCount')]
    'The number of times the video has been viewed.'
    like_count: Annotated[str, Field(alias='likeCount')]
    'The number of users who have indicated that they liked the video.'
    favorite_count: Annotated[str, Field(alias='favoriteCount')]
    'The favoriteCount is deprecated and the value is now always set to 0.'
    comment_count: Annotated[str, Field(alias='commentCount')]
    'The number of comments for the video.'


class PaidProductPlacement(BaseSchema):
    has_paid_product_placement: Annotated[bool, Field(alias='hasPaidProductPlacement')]
    'Set to true if the content uses paid product placement.'


class PlayerDetails(BaseSchema):
    embed_html: Annotated[str, Field(alias='embedHtml')]
    'An <iframe> tag that embeds a player that plays the video.'
    embed_height: Annotated[int | None, Field(alias='embedHeight')] = None
    'The height of the embedded player returned in the player.embedHtml property.'
    embed_width: Annotated[int | None, Field(alias='embedWidth')] = None
    'The width of the embedded player returned in the player.embedHtml property.'


class TopicDetails(BaseSchema):
    topic_categories: Annotated[list[str] | None, Field(alias='topicCategories')] = None
    "A list of Wikipedia URLs that provide a high-level description of the video's content."  # noqa: E501


class RecordingDetails(BaseSchema):
    recording_date: Annotated[datetime | None, Field(alias='recordingDate')] = None
    'The date and time when the video was recorded.'


class LiveStreamingDetails(BaseSchema):
    actual_start_time: Annotated[datetime | None, Field(alias='actualStartTime')] = None
    'The time that the broadcast actually started.'
    actual_end_time: Annotated[datetime | None, Field(alias='actualEndTime')] = None
    'The time that the broadcast actually ended.'
    scheduled_start_time: Annotated[
        datetime | None, Field(alias='scheduledStartTime')
    ] = None
    'The time that the broadcast is scheduled to begin.'
    scheduled_end_time: Annotated[datetime | None, Field(alias='scheduledEndTime')] = (
        None
    )
    'The time that the broadcast is scheduled to end.'
    concurrent_viewers: Annotated[int | None, Field(alias='concurrentViewers')] = None
    'The number of viewers currently watching the broadcast.'
    active_live_chat_id: Annotated[str | None, Field(alias='activeLiveChatId')] = None
    'The ID of the currently active live chat attached to this video.'


class YoutubeVideo(BaseSchema):
    kind: str
    "Identifies the API resource's type. The value will be youtube#video."
    etag: str
    'The Etag of this resource.'
    id: str
    'The ID that YouTube uses to uniquely identify the video.'
    snippet: VideoSnippet | None = None
    'The snippet object contains basic details about the video, such as its title, description, and category.'  # noqa: E501
    content_details: Annotated[ContentDetails | None, Field(alias='contentDetails')] = (
        None
    )
    'The contentDetails object contains information about the video content, including the length of the video and an indication of whether captions are available for the video.'  # noqa: E501
    status: VideoStatus | None = None
    "The status object contains information about the video's uploading, processing, and privacy statuses."  # noqa: E501
    statistics: Statistics | None = None
    'The statistics object contains statistics about the video.'
    paid_product_placement_details: Annotated[
        PaidProductPlacement | None, Field(alias='paidProductPlacementDetails')
    ] = None
    'The paidProductPlacementDetails object contains information about paid product placement in the video.'  # noqa: E501
    player: PlayerDetails | None = None
    'The player object contains information that you would use to play the video in an embedded player.'  # noqa: E501
    topic_details: Annotated[TopicDetails | None, Field(alias='topicDetails')] = None
    'The topicDetails object encapsulates information about topics associated with the video.'  # noqa: E501
    recording_details: Annotated[
        RecordingDetails | None, Field(alias='recordingDetails')
    ] = None
    'The recordingDetails object encapsulates information about the location, date and address where the video was recorded.'  # noqa: E501
    live_streaming_details: Annotated[
        LiveStreamingDetails | None, Field(alias='liveStreamingDetails')
    ] = None
    'The liveStreamingDetails object contains metadata about a live video broadcast.'
    localizations: Annotated[
        dict[str, LocalizedSnippet] | None, Field(alias='localizations')
    ] = None
    "The localizations object contains translations of the video's metadata."
