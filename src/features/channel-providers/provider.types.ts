import { ChannelId } from '@/features/channel/types'
import { ProviderBot } from '@/features/provider-bot/provider-bot.types'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type ChannelProviderId = Branded<string, 'ChannelProviderId'>

export interface ChannelProvider {
    id: ChannelProviderId
    channel_id: ChannelId
    provider: Provider
    name: string | null
    scope_needed: boolean
    bot_provider: ProviderBot | null
}

export const channelProviderLabels: { [provider: string | Provider]: string } =
    {
        twitch: 'Twitch',
        spotify: 'Spotify',
    } as const
