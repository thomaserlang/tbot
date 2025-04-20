from datetime import datetime
from typing import Annotated

from pydantic import Field

from tbot2.common import BaseRequestSchema, BaseSchema


class IngestionInfo(BaseSchema):
    stream_name: Annotated[str, Field(alias='streamName')]
    ingestion_address: Annotated[str, Field(alias='ingestionAddress')]
    backup_ingestion_address: Annotated[str, Field(alias='backupIngestionAddress')]


class CDN(BaseSchema):
    ingestion_type: Annotated[str, Field(alias='ingestionType')]
    ingestion_info: Annotated[IngestionInfo, Field(alias='ingestionInfo')]
    resolution: Annotated[str, Field(alias='resolution')]
    frame_rate: Annotated[str, Field(alias='frameRate')]


class Snippet(BaseSchema):
    published_at: Annotated[datetime, Field(alias='publishedAt')]
    channel_id: Annotated[str, Field(alias='channelId')]
    title: Annotated[str, Field(alias='title')]
    description: Annotated[str, Field(alias='description')]


class ConfigurationIssue(BaseSchema):
    type: Annotated[str, Field(alias='type')]
    severity: Annotated[str, Field(alias='severity')]
    reason: Annotated[str, Field(alias='reason')]
    description: Annotated[str, Field(alias='description')]


class HealthStatus(BaseSchema):
    status: Annotated[str | None, Field(alias='status')]
    last_update_time_seconds: Annotated[
        int | None, Field(alias='lastUpdateTimeSeconds')
    ] = None
    configuration_issues: Annotated[
        list[ConfigurationIssue] | None, Field(alias='configurationIssues')
    ] = None


class Status(BaseSchema):
    stream_status: Annotated[str, Field(alias='streamStatus')]
    health_status: Annotated[HealthStatus, Field(alias='healthStatus')]


class ContentDetails(BaseSchema):
    closed_captions_ingestion_url: Annotated[
        str, Field(alias='closedCaptionsIngestionUrl')
    ]
    is_reusable: Annotated[bool, Field(alias='isReusable')]


class LiveStream(BaseSchema):
    kind: Annotated[str, Field(alias='kind')]
    etag: Annotated[str, Field(alias='etag')]
    id: Annotated[str, Field(alias='id')]
    snippet: Annotated[Snippet | None, Field(alias='snippet')] = None
    cdn: Annotated[CDN | None, Field(alias='cdn')] = None
    status: Annotated[Status | None, Field(alias='status')] = None
    content_details: Annotated[ContentDetails | None, Field(alias='contentDetails')] = (
        None
    )


class LiveStreamInsertSnippet(BaseRequestSchema):
    """
    Basic details required for creating a live stream.
    """

    title: Annotated[
        str, Field(alias='title', description="The stream's title (1–128 characters).")
    ]
    description: Annotated[
        str | None,
        Field(
            alias='description',
            description="The stream's description (up to 10 000 characters).",
        ),
    ] = None


class LiveStreamInsertCDN(BaseRequestSchema):
    """
    CDN settings required to configure how YouTube ingests your stream.
    """

    ingestion_type: Annotated[
        str,
        Field(
            alias='ingestionType',
            description='The protocol used to transmit the video (dash, hls, rtmp).',
        ),
    ]
    resolution: Annotated[
        str,
        Field(
            alias='resolution',
            description='The resolution of the inbound video '
            '(e.g., 240p–2160p or variable).',
        ),
    ]
    frame_rate: Annotated[
        str,
        Field(
            alias='frameRate',
            description='The frame rate of the inbound video '
            '(e.g., 30fps, 60fps, or variable).',
        ),
    ]


class LiveStreamInsertContentDetails(BaseRequestSchema):
    """
    Optional settings for stream reusability.
    """

    is_reusable: Annotated[
        bool | None,
        Field(
            alias='isReusable',
            description='Indicates whether the stream can be bound to '
            'multiple broadcasts.',
        ),
    ] = None


class LiveStreamInsert(BaseRequestSchema):
    """
    Request body for creating a new YouTube liveStream via `liveStreams.insert`.
    Only the snippet, cdn, and contentDetails parts are allowed.
    """

    snippet: Annotated[
        LiveStreamInsertSnippet,
        Field(alias='snippet', description='Basic details about the stream.'),
    ]
    cdn: Annotated[
        LiveStreamInsertCDN,
        Field(alias='cdn', description='CDN configuration for video ingestion.'),
    ]
    content_details: Annotated[
        LiveStreamInsertContentDetails | None,
        Field(
            alias='contentDetails',
            description='Additional settings, such as stream reusability.',
        ),
    ] = None
