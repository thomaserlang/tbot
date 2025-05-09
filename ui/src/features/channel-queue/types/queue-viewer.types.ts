import { ProviderViewerId } from '@/features/channel-viewer'
import { ChannelId } from '@/features/channel/types/channel.types'
import { DateTimeString } from '@/types/datetime.type'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type ChannelQueueViewerId = Branded<string, 'ChannelQueueViewerId'>

export interface QueueViewer {
    id: ChannelQueueViewerId
    channel_id: ChannelId
    position: number
    provider: Provider
    provider_viewer_id: ProviderViewerId
    display_name: string
    created_at: DateTimeString
}

export interface QueueViewerCreate {
    provider: Provider
    provider_viewer_id: ProviderViewerId
    display_name: string
}
