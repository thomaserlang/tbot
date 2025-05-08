import { ChannelId } from '@/features/channel/types'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { useInfiniteQuery } from '@tanstack/react-query'
import { Queue } from '../types/queue.types'

interface GetParams {}

interface GetProps {
    channelId: ChannelId
    params?: GetParams
}

export function getQueuesQueryKey({ channelId, params }: GetProps) {
    return ['channel-queues', channelId, params]
}

export async function getChannelQueues({
    channelId,
}: GetProps & { params?: GetParams & { cursor?: string } }) {
    const r = await api.get<PageCursor<Queue>>(
        `/api/2/channels/${channelId}/queues`
    )
    return r.data
}

export function useGetQueues({ channelId, params }: GetProps) {
    return useInfiniteQuery({
        queryKey: getQueuesQueryKey({ channelId, params }),
        queryFn: ({ pageParam }) =>
            getChannelQueues({
                channelId,
                params: {
                    ...params,
                    cursor: pageParam,
                },
            }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
    })
}
