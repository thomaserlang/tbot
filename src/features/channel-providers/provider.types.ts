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
}
