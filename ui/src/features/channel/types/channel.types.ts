import { Feature } from '@/types/feature.type'
import { Branded } from '@/utils/brand'

export type ChannelId = Branded<string, 'CommandId'>
export type SubscriptionType = Branded<string, 'SubscriptionType'>

export interface Channel {
    id: ChannelId
    display_name: string
    subscription: SubscriptionType
    features: Feature[]
}
