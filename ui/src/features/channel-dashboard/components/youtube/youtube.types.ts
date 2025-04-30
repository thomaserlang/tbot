export interface Thumbnail {
    url: string
    width: number
    height: number
}

export interface LiveBroadcastSnippet {
    publishedAt: Date
    channelId: string
    title: string
    description: string
    thumbnails: Record<'default' | 'medium' | 'high' | string, Thumbnail>
    scheduledStartTime?: Date
    scheduledEndTime?: Date
    actualStartTime?: Date
    actualEndTime?: Date
    liveChatId: string
}

export interface LiveBroadcastStatus {
    lifeCycleStatus:
        | 'complete'
        | 'created'
        | 'live'
        | 'liveStarting'
        | 'ready'
        | 'revoked'
        | 'testStarting'
        | 'testing'
        | string
    privacyStatus: 'private' | 'public' | 'unlisted' | string
    recordingStatus: 'notRecording' | 'recording' | 'recorded' | string
    madeForKids?: boolean
    selfDeclaredMadeForKids?: boolean
}

export interface ContentDetailsMonitorStream {
    enableMonitorStream: boolean
    broadcastStreamDelayMs: number
    embedHtml: string
}

export interface ContentDetails {
    boundStreamId?: string
    boundStreamLastUpdateTimeMs?: Date
    monitorStream: ContentDetailsMonitorStream
    enableEmbed: boolean
    enableDvr: boolean
    recordFromStart: boolean
    enableClosedCaptions: boolean
    closedCaptionsType: string
    projection: string
    enableLowLatency: boolean
    latencyPreference: string
    enableAutoStart: boolean
    enableAutoStop: boolean
}

export interface CuePointSchedule {
    enabled: boolean
    pauseAdsUntil?: Date
    scheduleStrategy?: string
    repeatIntervalSecs?: number
}

export interface MonetizationDetails {
    cuepointSchedule: CuePointSchedule
}

export interface LiveBroadcast {
    kind: string
    etag: string
    id: string
    snippet: LiveBroadcastSnippet
    status: LiveBroadcastStatus
    contentDetails?: ContentDetails
    monetizationDetails?: MonetizationDetails
}

export interface LiveBroadcastInsertSnippet {
    title: string
    scheduledStartTime?: Date
    description?: string
    scheduledEndTime?: Date
}

export interface LiveBroadcastInsertStatus {
    privacyStatus: string
    selfDeclaredMadeForKids?: boolean
}

export interface MonitorStream {
    enableMonitorStream?: boolean
    broadcastStreamDelayMs?: number
}

export interface LiveBroadcastInsertContentDetails {
    monitorStream?: MonitorStream
    enableAutoStart?: boolean
    enableAutoStop?: boolean
    enableClosedCaptions?: boolean
    enableDvr?: boolean
    enableEmbed?: boolean
    recordFromStart?: boolean
}

export interface LiveBroadcastInsert {
    snippet: LiveBroadcastInsertSnippet
    status: LiveBroadcastInsertStatus
    contentDetails?: LiveBroadcastInsertContentDetails
}

export type LiveBroadcastUpdate = LiveBroadcastInsert
