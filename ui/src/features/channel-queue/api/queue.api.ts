import { ChannelId } from '@/features/channel/types/channel.types'
import { queryClient } from '@/queryclient'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { addRecord, removeRecord, updateRecord } from '@/utils/page-records'
import { InfiniteData, useMutation, useQuery } from '@tanstack/react-query'
import { ChannelQueueViewerId } from '../types/queue-viewer.types'
import {
    ChannelQueueId,
    Queue,
    QueueCreate,
    QueueUpdate,
} from '../types/queue.types'
import { getQueuesQueryKey } from './queues.api'

interface GetProps {
    channelId: ChannelId
    queueId: ChannelQueueId
}

export function getQueueQueryKey({ queueId }: Omit<GetProps, 'channelId'>) {
    return ['channel-queue', queueId]
}

export async function getQueue({ channelId, queueId }: GetProps) {
    const r = await api.get<Queue>(
        `/api/2/channels/${channelId}/queues/${queueId}`
    )
    return r.data
}

export function useGetQueue({ channelId, queueId }: GetProps) {
    return useQuery({
        queryKey: getQueueQueryKey({ queueId }),
        queryFn: () => getQueue({ channelId, queueId }),
    })
}

interface CreateProps {
    channelId: ChannelId
    data: QueueCreate
}

export async function createQueue({ channelId, data }: CreateProps) {
    const r = await api.post<Queue>(`/api/2/channels/${channelId}/queues`, data)
    queryClient.setQueryData(
        getQueueQueryKey({
            queueId: r.data.id,
        }),
        data
    )
    queryClient.setQueryData(
        getQueuesQueryKey({
            channelId,
        }),
        (oldData: InfiniteData<PageCursor<Queue>>) =>
            addRecord({
                oldData,
                data: r.data,
            })
    )
    return r.data
}

export function useCreateQueue({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: Queue, variables: CreateProps) => void
    onError?: (error: any, variables: CreateProps) => void
} = {}) {
    return useMutation({
        mutationFn: createQueue,
        onSuccess,
        onError,
    })
}

interface UpdateProps {
    channelId: ChannelId
    queueId: ChannelQueueId
    channelQueueViewerId: ChannelQueueViewerId
    data: QueueUpdate
}

export async function updateQueue({ channelId, queueId, data }: UpdateProps) {
    const r = await api.put<Queue>(
        `/api/2/channels/${channelId}/queues/${queueId}`,
        data
    )
    queryClient.setQueryData(
        getQueueQueryKey({
            queueId: r.data.id,
        }),
        r.data
    )
    queryClient.setQueryData(
        getQueuesQueryKey({
            channelId,
        }),
        (oldData: InfiniteData<PageCursor<Queue>>) =>
            updateRecord({
                oldData,
                data: r.data,
                matchFn: (item) => item.id === queueId,
            })
    )
    return r.data
}

export function useUpdateQueue({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: Queue, variables: UpdateProps) => void
    onError?: (error: any, variables: UpdateProps) => void
} = {}) {
    return useMutation({
        mutationFn: updateQueue,
        onSuccess: (data, variables) => {
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface DeleteProps {
    channelId: ChannelId
    queueId: ChannelQueueId
}

export async function deleteChannelQueue({ channelId, queueId }: DeleteProps) {
    await api.delete(`/api/2/channels/${channelId}/queues/${queueId}`)
    queryClient.setQueryData(
        getQueuesQueryKey({
            channelId: channelId,
        }),
        (oldData: InfiniteData<PageCursor<Queue>>) =>
            removeRecord({
                oldData,
                matchFn: (item) => item.id === queueId,
            })
    )
}

export function useDeleteQueue({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: any, variables: DeleteProps) => void
} = {}) {
    return useMutation({
        mutationFn: deleteChannelQueue,
        onSuccess,
        onError,
    })
}
