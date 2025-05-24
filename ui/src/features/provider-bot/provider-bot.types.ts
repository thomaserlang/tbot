import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type BotProviderId = Branded<string, 'BotProviderId'>

export interface ProviderBot {
    id: BotProviderId
    provider: Provider
    name: string
    provider_channel_id: string | null
    scope: string | null
    scope_needed: boolean
}
