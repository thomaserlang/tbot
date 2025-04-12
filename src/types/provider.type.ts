export type Provider = 'twitch' | 'youtube' | 'discord' | 'spotify'

export const providerLabels: { [key: string | Provider]: string } = {
    all: 'All',
    twitch: 'Twitch',
    youtube: 'YouTube',
    discord: 'Discord',
    spotify: 'Spotify',
} as const
