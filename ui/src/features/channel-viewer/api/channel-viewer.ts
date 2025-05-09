import { ChannelId } from '@/features/channel/types/channel.types'
import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { ChannelViewer, ProviderViewerId } from '../types/viewer.type'

export function getChannelViewerQueryKey(
    provider: Provider,
    channelId: ChannelId,
    providerViewerId: ProviderViewerId
) {
    return ['chanel-viewer', provider, channelId, providerViewerId]
}

export async function getChannelViewer(
    provider: Provider,
    channelId: ChannelId,
    providerViewerId: ProviderViewerId
) {
    const r = await api.get<ChannelViewer>(
        `/api/2/channels/${channelId}/viewers/${provider}/${providerViewerId}`
    )
    return r.data
}

interface GetProps {
    provider: Provider
    channelId: ChannelId
    providerViewerId: ProviderViewerId
}

export function useGetChannelViewer({
    provider,
    channelId,
    providerViewerId,
}: GetProps) {
    return useQuery({
        queryKey: getChannelViewerQueryKey(
            provider,
            channelId,
            providerViewerId
        ),
        queryFn: () => getChannelViewer(provider, channelId, providerViewerId),
    })
}
