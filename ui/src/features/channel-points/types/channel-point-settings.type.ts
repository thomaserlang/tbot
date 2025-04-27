import { ChannelId } from '@/features/channel/types'

export interface ChannelPointSettings {
    channel_id: ChannelId
    enabled: boolean
    points_name: string
    points_per_min: number
    points_per_min_sub_multiplier: number
    points_per_sub: number
    points_per_cheer: number
    ignore_users: string[]
}

export interface ChannelPointSettingsUpdate
    extends Omit<Partial<ChannelPointSettings>, 'channel_id'> {}
