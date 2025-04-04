export type Provider = 'twitch' | 'youtube' | 'discord'

export const providerLabels: { [key: string | Provider]: string } = {
    all: 'All',
    twitch: 'Twitch',
    youtube: 'YouTube',
    discord: 'Discord',
} as const
