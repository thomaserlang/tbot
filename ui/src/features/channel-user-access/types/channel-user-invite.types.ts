import { ChannelId } from '@/features/channel'
import { AccessLevel } from '@/types/access-level.type'
import { DateTimeString } from '@/types/datetime.type'
import { Branded } from '@/utils/brand'

export type ChannelUserInviteId = Branded<string, 'ChannelUserInviteId'>

export interface ChannelUserInvite {
    id: ChannelUserInviteId
    channel_id: ChannelId
    access_level: AccessLevel
    created_at: DateTimeString
    expires_at: DateTimeString
    expired: boolean
    invite_link: string
}

export interface ChannelUserInviteCreate {
    access_level: AccessLevel
}

export interface ChannelUserInviteUpdate extends ChannelUserInviteCreate {}
