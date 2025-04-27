import { ChannelProviderStream } from '@/features/channel-stream'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type ProviderViewerId = Branded<string, 'ProviderViewerId'>

export interface ViewerName {
    provider: Provider
    provider_viewer_id: ProviderViewerId
    name: string
    display_name: string
}

export interface ChannelViewerStats {
    viewer: ViewerName
    watchtime: number
    streams: number
    last_channel_provider_stream: ChannelProviderStream | null
}

export interface ChannelViewer {
    viewer: ViewerName
    stats: ChannelViewerStats
}

export interface StreamViewerWatchtime {
    channel_provider_stream_id: string
    provider_viewer_id: string
    watchtime: number
}

export interface ViewerStream {
    channel_provider_stream: ChannelProviderStream
    viewer_watchtime: StreamViewerWatchtime
}
