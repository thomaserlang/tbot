import { providerInfo } from '@/constants'
import { ChannelProvider } from './channel-provider.types'

export function getDashboardUrl(channelProvider: ChannelProvider) {
    if (
        channelProvider.stream_id &&
        providerInfo[channelProvider.provider].broadcastEditUrl
    ) {
        return providerInfo[channelProvider.provider].broadcastEditUrl?.replace(
            /{([^{}]+)}/g,
            (_, key) => (channelProvider[key] as string) || ''
        )
    }
    return providerInfo[channelProvider.provider].dashboardUrl?.replace(
        /{([^{}]+)}/g,
        (_, key) => (channelProvider[key] as string) || ''
    )
}
