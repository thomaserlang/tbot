import { ChannelId } from '@/features/channel/types/channel.types'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { useInfiniteQuery } from '@tanstack/react-query'
import { QueueViewer } from '../types/queue-viewer.types'
import { ChannelQueueId } from '../types/queue.types'

interface GetParams {}

interface GetProps {
    channelId: ChannelId
    queueId: ChannelQueueId
    params?: GetParams
}

export function getQueueViewersQueryKey({
    queueId,
    params = {},
}: Omit<GetProps, 'channelId'>) {
    return ['channel-queue', queueId, params]
}

export async function getQueueViewers({
    channelId,
    queueId: queueId,
}: GetProps & {
    params?: GetParams & { cursor?: string }
}): Promise<PageCursor<QueueViewer>> {
    const r = await api.get<PageCursor<QueueViewer>>(
        `/api/2/channels/${channelId}/queues/${queueId}/viewers`
    )
    return r.data
}

export function useGetQueueViewers({ channelId, queueId, params }: GetProps) {
    return useInfiniteQuery({
        queryKey: getQueueViewersQueryKey({
            queueId: queueId,
            params,
        }),
        queryFn: ({ pageParam }) =>
            getQueueViewers({
                channelId,
                queueId: queueId,
                params: {
                    ...params,
                    cursor: pageParam,
                },
            }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
        enabled: !!channelId && !!queueId,
    })
}
