import {
    IconBrandDiscord,
    IconBrandTwitch,
    IconBrandYoutube,
} from '@tabler/icons-react'
import { Provider, ProviderInfo } from './types/provider.type'

export const APP_TITLE = 'HEIMRA'

export const providerInfo: { [key: string | Provider]: ProviderInfo } = {
    twitch: {
        key: 'twitch',
        name: 'Twitch',
        color: '#6441a5',
        channelProvider: true,
        signinProvider: true,
        stream: true,
        chat: true,
        ownBot: true,
        systemBot: true,
        dashboardUrl:
            'https://dashboard.twitch.tv/u/{provider_user_name}/stream-manager',
        embedUrl:
            `https://player.twitch.tv/?channel={provider_user_name}` +
            `&parent=${window.location.hostname}&muted=true&autoplay=true`,
        streamTitleMaxLength: 140,
        chatIcon: <IconBrandTwitch size={18} />,
    },
    youtube: {
        key: 'youtube',
        name: 'YouTube',
        color: '#CD201F',
        channelProvider: true,
        signinProvider: true,
        stream: true,
        chat: true,
        ownBot: true,
        systemBot: true,
        dashboardUrl:
            'https://studio.youtube.com/channel/{provider_user_id}/livestreaming',
        broadcastEditUrl:
            'https://studio.youtube.com/video/{stream_id}/livestreaming',
        embedUrl: 'https://www.youtube.com/embed/{stream_id}?mute=1&autoplay=1',
        streamTitleMaxLength: 100,
        chatIcon: <IconBrandYoutube size={18} />,
    },
    spotify: {
        key: 'spotify',
        name: 'Spotify',
        channelProvider: true,
        stream: false,
        chat: false,
        ownBot: true,
        systemBot: false,
    },
    discord: {
        key: 'discord',
        name: 'Discord',
        color: '#7289da',
        chatIcon: <IconBrandDiscord size={18} />,
    },
} as const
