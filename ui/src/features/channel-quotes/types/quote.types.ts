import { ProviderViewerId } from '@/features/channel-viewer'
import { ChannelId } from '@/features/channel/types/channel.types'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type ChannelQuoteId = Branded<string, 'ChannelQuoteId'>

export interface ChannelQuote {
    id: ChannelQuoteId
    channel_id: ChannelId
    number: number
    message: string
    provider: Provider
    created_by_provider_viewer_id: ProviderViewerId
    created_by_display_name: string
    created_at: string
    updated_at: string | null
}

export interface ChannelQuoteCreate {
    message: string
    provider: Provider
    created_by_provider_viewer_id: string
    created_by_display_name: string
}

export interface ChannelQuoteUpdate extends Partial<ChannelQuoteCreate> {}
