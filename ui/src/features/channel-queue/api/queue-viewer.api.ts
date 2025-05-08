import { ChannelId } from '@/features/channel/types'
import { queryClient } from '@/queryclient'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { removeRecord } from '@/utils/page-records'
import { InfiniteData, useMutation } from '@tanstack/react-query'
import {
    ChannelQueueViewerId,
    QueueViewer,
    QueueViewerCreate,
} from '../types/queue-viewer.types'
import { ChannelQueueId } from '../types/queue.types'
import { getQueueViewersQueryKey } from './queue-viewers.api'

interface CreateProps {
    channelId: ChannelId
    queueId: ChannelQueueId
    data: QueueViewerCreate
}

export async function createQueueViewer({
    channelId,
    queueId,
    data,
}: CreateProps): Promise<QueueViewer> {
    const r = await api.post<QueueViewer>(
        `/api/2/channels/${channelId}/queues/${queueId}/viewers`,
        data
    )
    queryClient.invalidateQueries({
        queryKey: getQueueViewersQueryKey({
            queueId: queueId,
        }),
    })
    return r.data
}

export function useCreateQueueViewer({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: QueueViewerCreate, variables: CreateProps) => void
    onError?: (error: any, variables: CreateProps) => void
} = {}) {
    return useMutation({
        mutationFn: createQueueViewer,
        onSuccess,
        onError,
    })
}

interface MoveToTopProps {
    channelId: ChannelId
    queueId: ChannelQueueId
    data: {
        channelQueueViewerId: ChannelQueueViewerId
    }
}

export async function moveQueueViewerToTop({
    channelId,
    queueId,
    data,
}: MoveToTopProps): Promise<void> {
    await api.put(
        `/api/2/channels/${channelId}/queues/${queueId}/move-to-top`,
        {
            channel_queue_viewer_id: data.channelQueueViewerId,
        }
    )
    queryClient.invalidateQueries({
        queryKey: getQueueViewersQueryKey({
            queueId: queueId,
        }),
    })
}

export function useMoveQueueViewerToTop({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: MoveToTopProps) => void
    onError?: (error: any, variables: MoveToTopProps) => void
} = {}) {
    return useMutation({
        mutationFn: moveQueueViewerToTop,
        onSuccess,
        onError,
    })
}

interface DeleteProps {
    channelId: ChannelId
    queueId: ChannelQueueId
    queueViewerId: ChannelQueueViewerId
}

export async function deleteQueueViewer({
    channelId,
    queueId,
    queueViewerId,
}: DeleteProps): Promise<void> {
    await api.delete(
        `/api/2/channels/${channelId}/queues/${queueId}/viewers/${queueViewerId}`
    )
    queryClient.setQueriesData(
        {
            queryKey: getQueueViewersQueryKey({
                queueId: queueId,
            }),
        },
        (oldData: InfiniteData<PageCursor<QueueViewer>>) => {
            if (!oldData) return oldData
            return removeRecord({
                oldData,
                matchFn: (item) => item.id === queueViewerId,
            })
        }
    )
    queryClient.invalidateQueries({
        queryKey: getQueueViewersQueryKey({
            queueId: queueId,
        }),
    })
}

export function useDeleteQueueViewer({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: any, variables: DeleteProps) => void
} = {}) {
    return useMutation({
        mutationFn: deleteQueueViewer,
        onSuccess,
        onError,
    })
}

interface ClearQueueProps {
    channelId: ChannelId
    queueId: ChannelQueueId
}

export async function clearQueueViewers({
    channelId,
    queueId,
}: ClearQueueProps): Promise<void> {
    await api.delete(`/api/2/channels/${channelId}/queues/${queueId}/viewers`)

    queryClient.invalidateQueries({
        queryKey: getQueueViewersQueryKey({
            queueId: queueId,
        }),
    })
}

export function useClearQueueViewers({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: ClearQueueProps) => void
    onError?: (error: any, variables: ClearQueueProps) => void
} = {}) {
    return useMutation({
        mutationFn: clearQueueViewers,
        onSuccess,
        onError,
    })
}
