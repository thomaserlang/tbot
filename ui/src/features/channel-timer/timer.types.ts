import { ChannelId } from '@/features/channel'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type TimerId = Branded<string, 'TimerId'>

export type TimerPickMode = 'order' | 'random'
export const timerPickModeLabels: { [mode in TimerPickMode | string]: string } =
    {
        order: 'In Order',
        random: 'Random',
    } as const

export type TimerActiveMode = 'always' | 'online' | 'offline'
export const timerActiveModeLabels: {
    [mode in TimerActiveMode | string]: string
} = {
    always: 'Online & Offline',
    online: 'Online',
    offline: 'Offline',
} as const

export interface Timer {
    id: TimerId
    channel_id: ChannelId
    name: string
    messages: string[]
    interval: number
    enabled: boolean
    provider: Provider | 'all'
    pick_mode: TimerPickMode
    active_mode: TimerActiveMode
    next_run_at: string // ISO 8601 datetime
    last_message_index: number | null
    created_at: string // ISO 8601 datetime
    updated_at: string // ISO 8601 datetime
}

export interface TimerCreate {
    name: string
    messages: string[]
    interval: number
    enabled?: boolean
    provider?: Provider | 'all'
    pick_mode?: TimerPickMode
    active_mode?: TimerActiveMode
}

export interface TimerUpdate extends Partial<TimerCreate> {}
