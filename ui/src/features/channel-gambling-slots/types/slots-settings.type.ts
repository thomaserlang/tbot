import { ChannelId } from '@/features/channel/types/channel.types'

export interface SlotsSettings {
    channel_id: ChannelId
    emotes: string[]
    emote_pool_size: number
    payout_percent: number
    win_message: string
    lose_message: string
    allin_win_message: string
    allin_lose_message: string
    min_bet: number
    max_bet: number
}

export type SlotsSettingsUpdate = Omit<Partial<SlotsSettings>, 'channel_id'>
