import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'
import { ChannelId } from '../channel/types'

export type ChannelProviderId = Branded<string, 'ChannelProviderId'>

export interface ChannelProvider {
    id: ChannelProviderId
    channel_id: ChannelId
    provider: Provider
    name: string | null
    scope_needed: boolean
    bot_provider: BotProvider | null
}

export interface BotProvider {
    id: string
    name: string | null
    provider_user_id: string | null
    scope: string | null
    scope_needed: boolean
}

export const channelProviderLabels: { [provider: string | Provider]: string } =
    {
        twitch: 'Twitch',
    } as const
