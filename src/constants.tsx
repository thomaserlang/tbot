import { IconBrandTwitch, IconBrandYoutube } from '@tabler/icons-react'
import { Provider, ProviderInfo } from './types/provider.type'

export const APP_TITLE = 'HEIMRA'

export const providerInfo: { [key: string | Provider]: ProviderInfo } = {
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
        stream_title_max_length: 140,
        chat_icon: <IconBrandTwitch size={18} />,
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
        broadcast_edit_url:
            'https://studio.youtube.com/video/{stream_id}/livestreaming',
        embed_url:
            'https://www.youtube.com/embed/{stream_id}?mute=1&autoplay=1',
        stream_title_max_length: 100,
        chat_icon: <IconBrandYoutube size={18} />,
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
