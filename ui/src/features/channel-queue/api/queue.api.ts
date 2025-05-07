import { ChannelId } from '@/features/channel/types'
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
    channelQueueId: ChannelQueueId
}

export function getQueueQueryKey({ channelId, channelQueueId }: GetProps) {
    return ['channel-queue', channelId, channelQueueId]
}

export async function getQueue({ channelId, channelQueueId }: GetProps) {
    const r = await api.get<Queue>(
        `/api/2/channels/${channelId}/queues/${channelQueueId}`
    )
    return r.data
}

export function useGetQueue({ channelId, channelQueueId }: GetProps) {
    return useQuery({
        queryKey: getQueueQueryKey({ channelId, channelQueueId }),
        queryFn: () => getQueue({ channelId, channelQueueId }),
    })
}

interface CreateProps {
    channelId: ChannelId
    data: QueueCreate
}

export async function createQueue({ channelId, data }: CreateProps) {
    const r = await api.post<Queue>(`/api/2/channels/${channelId}/queues`, data)
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
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getQueueQueryKey({
                    channelId: variables.channelId,
                    channelQueueId: data.id,
                }),
                data
            )
            queryClient.setQueryData(
                getQueuesQueryKey({
                    channelId: variables.channelId,
                }),
                (oldData: InfiniteData<PageCursor<Queue>>) =>
                    addRecord({
                        oldData,
                        data,
                    })
            )
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface UpdateProps {
    channelId: ChannelId
    channelQueueId: ChannelQueueId
    channelQueueViewerId: ChannelQueueViewerId
    data: QueueUpdate
}

export async function updateQueue({
    channelId,
    channelQueueId,
    data,
}: UpdateProps) {
    const r = await api.put<Queue>(
        `/api/2/channels/${channelId}/queues/${channelQueueId}`,
        data
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
            queryClient.setQueryData(
                getQueueQueryKey({
                    channelId: variables.channelId,
                    channelQueueId: data.id,
                }),
                data
            )
            queryClient.setQueryData(
                getQueuesQueryKey({
                    channelId: variables.channelId,
                }),
                (oldData: InfiniteData<PageCursor<Queue>>) =>
                    updateRecord({
                        oldData,
                        data,
                        matchFn: (item) => item.id === data.id,
                    })
            )
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface DeleteProps {
    channelId: ChannelId
    channelQueueId: ChannelQueueId
}

export async function deleteQueue({ channelId, channelQueueId }: DeleteProps) {
    await api.delete(`/api/2/channels/${channelId}/queues/${channelQueueId}`)
}

export function useDeleteQueue({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: any, variables: DeleteProps) => void
} = {}) {
    return useMutation({
        mutationFn: deleteQueue,
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getQueueQueryKey({
                    channelId: variables.channelId,
                    channelQueueId: variables.channelQueueId,
                }),
                data
            )
            queryClient.setQueryData(
                getQueuesQueryKey({
                    channelId: variables.channelId,
                }),
                (oldData: InfiniteData<PageCursor<Queue>>) =>
                    removeRecord({
                        oldData,
                        matchFn: (item) => item.id === variables.channelQueueId,
                    })
            )
            onSuccess?.(data, variables)
        },
        onError,
    })
}
