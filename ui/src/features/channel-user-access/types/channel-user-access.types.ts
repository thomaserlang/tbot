import { ChannelId } from '@/features/channel/types/channel.types'
import { User } from '@/features/user'
import { AccessLevel } from '@/types/access-level.type'
import { Branded } from '@/utils/brand'

export type ChannelUserAccessId = Branded<string, 'ChannelUserAccessId'>

export interface ChannelUserAccess {
    id: ChannelUserAccessId
    channel_id: ChannelId
    user: User
    access_level: AccessLevel
}
