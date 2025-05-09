import { ChannelId } from '@/features/channel/types/channel.types'
import { ProviderBot } from '@/features/provider-bot/provider-bot.types'
import { Provider } from '@/types/provider.type'
import { Thumbnail } from '@/types/thumbnail.type'
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
        | Thumbnail
    id: ChannelProviderId
    channel_id: ChannelId
    provider: Provider
    provider_user_id: string | null
    provider_user_name: string | null
    provider_user_display_name: string | null
    scope_needed: boolean
    bot_provider: ProviderBot | null
    stream_title: string | null
    stream_id: string | null
    stream_live: boolean
    stream_live_at: string | null
}
