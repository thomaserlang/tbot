import { ReactNode } from 'react'

export type Provider = 'twitch' | 'youtube' | 'discord' | 'spotify'

export interface ProviderInfo {
    [key: string]: string | boolean | Provider | undefined | number | ReactNode
    key: Provider
    name: string
    color?: string
    stream?: boolean
    chat?: boolean
    own_bot?: boolean
    system_bot?: boolean
    dashboard_url?: string
    embed_url?: string
    broadcast_edit_url?: string
    stream_title_max_length?: number
    chat_icon?: ReactNode
}
