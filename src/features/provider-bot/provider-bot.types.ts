import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type BotProviderId = Branded<string, 'BotProviderId'>

export interface ProviderBot {
    id: BotProviderId
    provider: Provider
    name: string
    provider_user_id: string | null
    scope: string | null
    scope_needed: boolean
}

export const providerBotLabels: { [provider: string | Provider]: string } = {
    twitch: 'Twitch',
    youtube: 'YouTube',
} as const
