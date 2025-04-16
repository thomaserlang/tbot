import { ChannelId } from '@/features/channel'
import { PageCursor } from '@/types/page-cursor.type'
import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { useInfiniteQuery } from '@tanstack/react-query'
import { ProviderViewerId, ViewerStream } from '../types/viewer.type'

interface Params {
    per_page?: number
}

export function getChannelViewerStreamsQueryKey(
    provider: Provider,
    channelId: ChannelId,
    providerViewerId: ProviderViewerId,
    params?: Params
) {
    return [
        'channel-viewer-streams',
        provider,
        channelId,
        providerViewerId,
        params,
    ]
}

export async function getChannelViewerStreams(
    provider: Provider,
    channelId: ChannelId,
    providerViewerId: ProviderViewerId,
    params?: Params & {
        cursor?: string
    }
) {
    const r = await api.get<PageCursor<ViewerStream>>(
        `/api/2/channels/${channelId}/viewers/${provider}/${providerViewerId}/streams`,
        {
            params,
        }
    )
    return r.data
}

interface GetProps {
    provider: Provider
    channelId: ChannelId
    providerViewerId: ProviderViewerId
    params?: Params
}

export function useGetChannelViewerStreams({
    provider,
    channelId,
    providerViewerId,
    params,
}: GetProps) {
    return useInfiniteQuery({
        queryKey: getChannelViewerStreamsQueryKey(
            provider,
            channelId,
            providerViewerId,
            params
        ),
        queryFn: ({ pageParam }) =>
            getChannelViewerStreams(provider, channelId, providerViewerId, {
                ...params,
                cursor: pageParam,
            }),
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
        initialPageParam: '',
    })
}
