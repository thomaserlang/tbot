import { providerInfo } from '@/constants'
import { ChannelProvider } from '../channel-provider.types'

interface Props {
    channelProvider: ChannelProvider
    height?: string
    width?: string
}

export function ChannelProviderEmbedLive({
    channelProvider,
    width = '100%',
    height,
}: Props) {
    if (!providerInfo[channelProvider.provider].embedUrl) return null
    if (!channelProvider.live_stream_id) return null
    return (
        <iframe
            width={width}
            height={height}
            src={providerInfo[channelProvider.provider].embedUrl?.replace(
                /{([^{}]+)}/g,
                (_, key) => (channelProvider[key] as string) || ''
            )}
            referrerPolicy="strict-origin-when-cross-origin"
            frameBorder="0"
            allowFullScreen
        ></iframe>
    )
}
