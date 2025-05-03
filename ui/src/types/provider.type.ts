import { ReactNode } from 'react'

export type Provider = 'twitch' | 'youtube' | 'discord' | 'spotify' | 'tiktok'

export interface ProviderInfo {
    [key: string]: string | boolean | Provider | undefined | number | ReactNode
    key: Provider
    name: string
    channelProvider?: boolean
    signinProvider?: boolean
    color?: string
    stream?: boolean
    chat_read?: boolean
    chat_write?: boolean
    ownBot?: boolean
    systemBot?: boolean
    dashboardUrl?: string
    embedUrl?: string
    broadcastEditUrl?: string
    streamTitleMaxLength?: number
    icon?: ReactNode
}
