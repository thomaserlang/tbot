import { ChannelId } from '@/features/channel/types/channel.types'
import { ProviderBot } from '@/features/provider-bot/provider-bot.types'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type ChannelProviderId = Branded<string, 'ChannelProviderId'>

export interface ChannelProvider {
    [key: string]:
        | ChannelProviderId
        | ChannelId
        | Provider
        | string
        | null
        | boolean
        | ProviderBot
        | number
    id: ChannelProviderId
    channel_id: ChannelId
    provider: Provider
    provider_channel_id: string | null
    provider_channel_name: string | null
    provider_channel_display_name: string | null
    scope_needed: boolean
    bot_provider: ProviderBot | null
    stream_title: string | null
    live_stream_id: string | null
    stream_live: boolean
    stream_live_at: string | null
    stream_viewer_count: number | null
    channel_provider_stream_id: string | null
}
