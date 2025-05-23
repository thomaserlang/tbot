import { ChannelId } from '@/features/channel/types/channel.types'

export interface EmulateEvent {
    name: string
    request: ({ channelId }: { channelId: ChannelId }) => Promise<any>
}
