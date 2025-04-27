import { ChannelId } from '@/features/channel/types'

export interface RouletteSettings {
    channel_id: ChannelId
    win_chance: number
    win_message: string
    lose_message: string
    allin_win_message: string
    allin_lose_message: string
    min_bet: number
    max_bet: number
}

export type RouletteSettingsUpdate = Omit<
    Partial<RouletteSettings>,
    'channel_id'
>
