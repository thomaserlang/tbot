import { ChannelId } from '@/features/channel/types'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { useInfiniteQuery } from '@tanstack/react-query'
import { QueueViewer } from '../types/queue-viewer.types'
import { ChannelQueueId } from '../types/queue.types'

interface GetParams {}

interface GetProps {
    channelId: ChannelId
    channelQueueId: ChannelQueueId
    params?: GetParams
}

export function getQueueViewersQueryKey({
    channelId,
    channelQueueId,
}: GetProps) {
    return ['channel-queue-viewers', channelId, channelQueueId]
}

export async function getQueueViewers({
    channelId,
    channelQueueId,
}: GetProps & {
    params?: GetParams & { cursor?: string }
}): Promise<PageCursor<QueueViewer>> {
    const r = await api.get<PageCursor<QueueViewer>>(
        `/api/2/channels/${channelId}/queues/${channelQueueId}/viewers`
    )
    return r.data
}

export function useGetQueueViewers({
    channelId,
    channelQueueId,
    params,
}: GetProps) {
    return useInfiniteQuery({
        queryKey: getQueueViewersQueryKey({
            channelId,
            channelQueueId,
            params,
        }),
        queryFn: ({ pageParam }) =>
            getQueueViewers({
                channelId,
                channelQueueId,
                params: {
                    ...params,
                    cursor: pageParam,
                },
            }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
    })
}
