import { ChannelId } from '@/features/channel/types'
import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { ChannelViewer, ProviderViewerId } from '../types/viewer.type'

export function getChannelViewerQueryKey(
    provider: Provider,
    channelId: ChannelId,
    viewerId: ProviderViewerId
) {
    return ['chanel-viewer', provider, channelId, viewerId]
}

export async function getChannelViewer(
    provider: Provider,
    channelId: ChannelId,
    viewerId: ProviderViewerId
) {
    const r = await api.get<ChannelViewer>(
        `/api/2/channels/${channelId}/viewers/${provider}/${viewerId}`
    )
    return r.data
}

interface GetProps {
    provider: Provider
    channelId: ChannelId
    viewerId: ProviderViewerId
}

export function useGetChannelViewer({
    provider,
    channelId,
    viewerId,
}: GetProps) {
    return useQuery({
        queryKey: getChannelViewerQueryKey(provider, channelId, viewerId),
        queryFn: () => getChannelViewer(provider, channelId, viewerId),
    })
}
