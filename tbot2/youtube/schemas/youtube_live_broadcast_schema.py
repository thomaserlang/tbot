from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field

from tbot2.common import BaseSchema


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
    thumbnails: dict[Literal['default', 'medium', 'high', 'standard'] | str, Thumbnail]
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
    made_for_kids: Annotated[bool, Field(alias='madeForKids')]
    self_declared_made_for_kids: Annotated[bool, Field(alias='selfDeclaredMadeForKids')]


class ContentDetailsMonitorSream(BaseSchema):
    enable_monitor_stream: Annotated[bool, Field(alias='enableMonitorStream')]
    broadcast_stream_delay_ms: Annotated[int, Field(alias='broadcastStreamDelayMs')]
    embedeHtml: Annotated[str, Field(alias='embedHtml')]


class ContentDetails(BaseSchema):
    bound_stream_id: Annotated[str, Field(alias='boundStreamId')]
    bound_stream_last_update_time_ms: Annotated[
        datetime, Field(alias='boundStreamLastUpdateTimeMs')
    ]
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
    content_details: Annotated[ContentDetails, Field(alias='contentDetails')]
    monetization_details: Annotated[
        MonetizationDetails, Field(alias='monetizationDetails')
    ]
