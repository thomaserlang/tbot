import {
    IconBrandDiscord,
    IconBrandTiktok,
    IconBrandTwitch,
    IconBrandYoutube,
} from '@tabler/icons-react'
import { Provider, ProviderInfo } from '../types/provider.type'

export const providerInfo: { [key in Provider]: ProviderInfo } = {
    twitch: {
        key: 'twitch',
        name: 'Twitch',
        color: '#6441a5',
        channelProvider: true,
        signinProvider: true,
        stream: true,
        chat_read: true,
        chat_write: true,
        ownBot: true,
        systemBot: true,
        dashboardUrl:
            'https://dashboard.twitch.tv/u/{provider_user_name}/stream-manager',
        embedUrl:
            `https://player.twitch.tv/?channel={provider_user_name}` +
            `&parent=${window.location.hostname}&muted=true&autoplay=true`,
        streamTitleMaxLength: 140,
        icon: <IconBrandTwitch size={18} />,
    },
    youtube: {
        key: 'youtube',
        name: 'YouTube',
        color: '#CD201F',
        channelProvider: true,
        signinProvider: true,
        stream: true,
        chat_read: true,
        chat_write: true,
        ownBot: true,
        systemBot: true,
        dashboardUrl:
            'https://studio.youtube.com/channel/{provider_user_id}/livestreaming',
        broadcastEditUrl:
            'https://studio.youtube.com/video/{live_stream_id}/livestreaming',
        embedUrl:
            'https://www.youtube.com/embed/{live_stream_id}?mute=1&autoplay=1',
        streamTitleMaxLength: 100,
        icon: <IconBrandYoutube size={18} />,
    },
    tiktok: {
        key: 'tiktok',
        name: 'TikTok',
        color: '#010101',
        channelProvider: true,
        stream: true,
        chat_read: true,
        icon: <IconBrandTiktok color="white" size={18} />,
    },
    spotify: {
        key: 'spotify',
        name: 'Spotify',
        channelProvider: true,
        stream: false,
        chat_read: false,
        ownBot: true,
        systemBot: false,
    },
    discord: {
        key: 'discord',
        name: 'Discord',
        color: '#7289da',
        icon: <IconBrandDiscord size={18} />,
    },
} as const
