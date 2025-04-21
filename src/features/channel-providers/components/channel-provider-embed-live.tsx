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
    if (!providerInfo[channelProvider.provider].embed_url) return null
    if (!channelProvider.stream_id) return null
    return (
        <iframe
            width={width}
            height={height}
            src={providerInfo[channelProvider.provider].embed_url?.replace(
                /{([^{}]+)}/g,
                (_, key) => (channelProvider[key] as string) || ''
            )}
            referrerPolicy="strict-origin-when-cross-origin"
            frameBorder="0"
            allowFullScreen
        ></iframe>
    )
}
