import { Branded } from '@/utils/brand'

export type ChannelId = Branded<string, 'CommandId'>

export interface Channel {
    id: ChannelId
    display_name: string
}
