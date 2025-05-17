from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field

from tbot2.common import BaseRequestSchema, BaseSchema


class Thumbnail(BaseSchema):
    url: str
    width: int
    height: int


class LiveBroadcastSnippet(BaseSchema):
    published_at: Annotated[datetime, Field(alias='publishedAt')]
    channel_id: Annotated[
        str,
        Field(
            alias='channelId',
        ),
    ]
    """The ID that YouTube uses to uniquely identify the channel 
    that is publishing the broadcast."""
    title: str
    description: str
    thumbnails: dict[Literal['default', 'medium', 'high'] | str, Thumbnail]
    scheduled_start_time: Annotated[
        datetime | None, Field(alias='scheduledStartTime')
    ] = None
    scheduled_end_time: Annotated[datetime | None, Field(alias='scheduledEndTime')] = (
        None
    )
    actual_start_time: Annotated[datetime | None, Field(alias='actualStartTime')] = None
    actual_end_time: Annotated[datetime | None, Field(alias='actualEndTime')] = None
    live_chat_id: Annotated[str, Field(alias='liveChatId')]


class LiveBroadcastStatus(BaseSchema):
    life_cycle_status: Annotated[
        str
        | Literal[
            'complete',
            'created',
            'live',
            'liveStarting',
            'ready',
            'revoked',
            'testStarting',
            'testing',
        ],
        Field(alias='lifeCycleStatus'),
    ]
    privacy_status: Annotated[
        Literal['private', 'public', 'unlisted'] | str, Field(alias='privacyStatus')
    ]
    recording_status: Annotated[
        Literal['notRecording', 'recording', 'recorded'] | str,
        Field(alias='recordingStatus'),
    ]
    made_for_kids: Annotated[bool | None, Field(alias='madeForKids')] = None
    self_declared_made_for_kids: Annotated[
        bool | None, Field(alias='selfDeclaredMadeForKids')
    ] = None


class ContentDetailsMonitorSream(BaseSchema):
    enable_monitor_stream: Annotated[bool, Field(alias='enableMonitorStream')]
    broadcast_stream_delay_ms: Annotated[int, Field(alias='broadcastStreamDelayMs')]
    embedeHtml: Annotated[str, Field(alias='embedHtml')]


class ContentDetails(BaseSchema):
    bound_stream_id: Annotated[str | None, Field(alias='boundStreamId')] = None
    bound_stream_last_update_time_ms: Annotated[
        datetime | None, Field(alias='boundStreamLastUpdateTimeMs')
    ] = None
    monitor_stream: Annotated[ContentDetailsMonitorSream, Field(alias='monitorStream')]
    enable_embed: Annotated[bool, Field(alias='enableEmbed')]
    enable_dvr: Annotated[bool, Field(alias='enableDvr')]
    record_from_start: Annotated[bool, Field(alias='recordFromStart')]
    enable_closed_captions: Annotated[bool, Field(alias='enableClosedCaptions')]
    closed_captions_type: Annotated[str, Field(alias='closedCaptionsType')]
    projection: Annotated[str, Field(alias='projection')]
    enable_low_latency: Annotated[bool, Field(alias='enableLowLatency')]
    latency_preference: Annotated[str, Field(alias='latencyPreference')]
    enable_auto_start: Annotated[bool, Field(alias='enableAutoStart')]
    enable_auto_stop: Annotated[bool, Field(alias='enableAutoStop')]


class CuePointSchedule(BaseSchema):
    enabled: bool
    pause_ads_until: Annotated[datetime | None, Field(alias='pauseAdsUntil')] = None
    schedule_strategy: Annotated[str | None, Field(alias='scheduleStrategy')] = None
    repeat_interval_secs: Annotated[int | None, Field(alias='repeatIntervalSecs')] = (
        None
    )


class MonetizationDetails(BaseSchema):
    cuepoint_schedule: Annotated[CuePointSchedule, Field(alias='cuepointSchedule')]


class LiveBroadcast(BaseSchema):
    kind: str
    etag: str
    id: str
    'The ID that YouTube assigns to uniquely identify the broadcast.'
    snippet: LiveBroadcastSnippet
    status: LiveBroadcastStatus
    content_details: Annotated[ContentDetails | None, Field(alias='contentDetails')] = (
        None
    )
    monetization_details: Annotated[
        MonetizationDetails | None, Field(alias='monetizationDetails')
    ] = None


class LiveBroadcastInsertSnippet(BaseRequestSchema):
    """
    Basic details required to schedule a live broadcast.
    """

    title: Annotated[
        str,
        Field(alias='title', description="The broadcast's title (1-100 characters)."),
    ]
    scheduled_start_time: Annotated[
        datetime | None,
        Field(
            alias='scheduledStartTime',
            description='The time the broadcast is scheduled to start (ISO 8601).',
        ),
    ]
    description: Annotated[
        str | None,
        Field(
            alias='description',
            description="The broadcast's description (up to 5000 characters).",
        ),
    ] = None
    scheduled_end_time: Annotated[
        datetime | None,
        Field(
            alias='scheduledEndTime',
            description='The time the broadcast is scheduled to end (ISO 8601).',
        ),
    ] = None


class LiveBroadcastInsertStatus(BaseRequestSchema):
    """
    Privacy settings and made‑for‑kids flag for the broadcast.
    """

    privacy_status: Annotated[
        str,
        Field(
            alias='privacyStatus',
            description="Broadcast's privacy setting (private, public, or unlisted).",
        ),
    ]
    self_declared_made_for_kids: Annotated[
        bool | None,
        Field(
            alias='selfDeclaredMadeForKids',
            description='Whether the broadcast is marked as made for kids.',
        ),
    ] = None


class MonitorStream(BaseRequestSchema):
    """
    Settings for the broadcast's monitor stream.
    """

    enable_monitor_stream: Annotated[
        bool,
        Field(
            alias='enableMonitorStream',
            description='Whether to enable the monitor stream for the broadcast.',
        ),
    ] = True
    broadcast_stream_delay_ms: Annotated[
        int | None,
        Field(
            alias='broadcastStreamDelayMs',
            description='Delay in milliseconds for the monitor stream.',
        ),
    ] = None


class LiveBroadcastInsertContentDetails(BaseSchema):
    """
    Additional settings that control broadcast behavior.
    """

    monitor_stream: Annotated[
        MonitorStream | None,
        Field(
            alias='monitorStream',
            description="Settings for the broadcast's monitor stream.",
        ),
    ] = None
    enable_auto_start: Annotated[
        bool | None,
        Field(
            alias='enableAutoStart',
            description='Automatically start the broadcast when the stream goes live.',
        ),
    ] = None
    enable_auto_stop: Annotated[
        bool | None,
        Field(
            alias='enableAutoStop',
            description='Automatically stop the broadcast when the stream ends.',
        ),
    ] = None
    enable_closed_captions: Annotated[
        bool | None,
        Field(
            alias='enableClosedCaptions',
            description='Enable closed captions on the broadcast.',
        ),
    ] = None
    enable_dvr: Annotated[
        bool | None, Field(alias='enableDvr', description='Enable DVR functionality.')
    ] = None
    enable_embed: Annotated[
        bool | None,
        Field(
            alias='enableEmbed',
            description='Allow embedding of the broadcast on external sites.',
        ),
    ] = None
    record_from_start: Annotated[
        bool | None,
        Field(
            alias='recordFromStart',
            description='Record the broadcast from its very start.',
        ),
    ] = None


class LiveBroadcastInsert(BaseRequestSchema):
    """
    Request body for scheduling a new live broadcast via `liveBroadcasts.insert`.
    """

    snippet: Annotated[
        LiveBroadcastInsertSnippet,
        Field(alias='snippet', description='Basic broadcast details.'),
    ]
    status: Annotated[
        LiveBroadcastInsertStatus,
        Field(alias='status', description='Privacy settings and made‑for‑kids flag.'),
    ]
    content_details: Annotated[
        LiveBroadcastInsertContentDetails | None,
        Field(
            alias='contentDetails',
            description='Additional broadcast behavior settings.',
        ),
    ] = None


class LiveBroadcastUpdate(LiveBroadcastInsert): ...


class LiveBroadcastCuepoint(BaseSchema):
    id: Annotated[
        str | None, Field(description='Unique identifier for the cuepoint.')
    ] = None
    insertion_offset_time_ms: Annotated[
        int | None,
        Field(
            alias='insertionOffsetTimeMs',
            description=(
                'Time offset in milliseconds for cuepoint insertion. '
                'Must not be set if walltimeMs is set.'
            ),
        ),
    ] = None
    walltime_ms: Annotated[
        int | None,
        Field(
            alias='walltimeMs',
            description=(
                'Epoch timestamp (in milliseconds) for cuepoint insertion. '
                'Must not be set if insertionOffsetTimeMs is set.'
            ),
        ),
    ] = None
    duration_secs: Annotated[
        int | None,
        Field(
            alias='durationSecs',
            description='Cuepoint duration in seconds. Must be a positive integer.',
            ge=0,
        ),
    ] = 30
    cue_type: Annotated[
        Literal['cueTypeAd'] | str,
        Field(
            alias='cueType',
            description="Cuepoint type. Must be set to 'cueTypeAd'.",
        ),
    ]
