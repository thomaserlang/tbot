import React from 'react'

export type Provider = 'twitch' | 'youtube' | 'discord' | 'spotify' | 'tiktok'

interface IconProps extends React.ComponentPropsWithoutRef<'svg'> {
    size?: number | string
}

export interface ProviderInfo {
    [key: string]:
        | string
        | boolean
        | Provider
        | number
        | undefined
        | ((props: IconProps) => React.ReactElement)
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
    icon?: (props: IconProps) => React.ReactElement
}
