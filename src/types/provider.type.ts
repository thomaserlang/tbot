export type Provider = 'twitch' | 'youtube' | 'discord' | 'spotify'

export interface ProviderInfo {
    key: Provider
    name: string
    stream?: boolean
    chat?: boolean
    own_bot?: boolean
    system_bot?: boolean
}

export const providers: { [key: string | Provider]: ProviderInfo } = {
    twitch: {
        key: 'twitch',
        name: 'Twitch',
        stream: true,
        chat: true,
        own_bot: true,
        system_bot: true,
    },
    youtube: {
        key: 'youtube',
        name: 'YouTube',
        stream: true,
        chat: true,
        own_bot: true,
        system_bot: true,
    },
    spotify: {
        key: 'spotify',
        name: 'Spotify',
        stream: false,
        chat: false,
        own_bot: true,
        system_bot: false,
    },
} as const
