import { ChannelId } from '@/features/channel'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type ChannelProviderStreamId = Branded<string, 'ChannelProviderStreamId'>

export interface ChannelProviderStream {
    id: ChannelProviderStreamId
    channel_id: ChannelId
    channel_stream_id: string
    provider: Provider
    provider_channel_id: string
    provider_stream_id: string
    started_at: string
    ended_at: string | null
}
