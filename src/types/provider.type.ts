export type Provider = 'twitch' | 'youtube' | 'discord' | 'spotify'

export interface ProviderInfo {
    [key: string]: string | boolean | Provider | undefined
    key: Provider
    name: string
    color?: string
    stream?: boolean
    chat?: boolean
    own_bot?: boolean
    system_bot?: boolean
    dashboard_url?: string
    embed_url?: string
}

export const providers: { [key: string | Provider]: ProviderInfo } = {
    twitch: {
        key: 'twitch',
        name: 'Twitch',
        color: '#6441a5',
        stream: true,
        chat: true,
        own_bot: true,
        system_bot: true,
        dashboard_url:
            'https://dashboard.twitch.tv/u/{provider_user_name}/stream-manager',
        embed_url:
            `https://player.twitch.tv/?channel={provider_user_name}` +
            `&parent=${window.location.hostname}&muted=true&autoplay=true`,
    },
    youtube: {
        key: 'youtube',
        name: 'YouTube',
        color: '#CD201F',
        stream: true,
        chat: true,
        own_bot: true,
        system_bot: true,
        dashboard_url:
            'https://studio.youtube.com/channel/{provider_user_id}/livestreaming',
        embed_url:
            'https://www.youtube.com/embed/{stream_id}?mute=1&autoplay=1',
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
