import { ChannelId } from '@/features/channel/types'
import { DateTimeString } from '@/types/datetime.type'
import { Branded } from '@/utils/brand'

export type ChannelQueueId = Branded<string, 'ChannelQueueId'>

export interface Queue {
    id: ChannelQueueId
    channel_id: ChannelId
    name: string
    create_at: DateTimeString
}

export interface QueueCreate {
    name: string
}

export interface QueueUpdate extends Partial<QueueCreate> {}
