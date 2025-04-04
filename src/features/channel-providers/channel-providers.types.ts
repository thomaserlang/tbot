import { Branded } from '@/utils/brand'

export type ChannelProviderId = Branded<string, 'ChannelProviderId'>

export interface ChannelProvider {
    id: ChannelProviderId
    provider: string
    name: string | null
}
