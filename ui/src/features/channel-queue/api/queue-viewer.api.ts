import { ChannelId } from '@/features/channel/types'
import { queryClient } from '@/queryclient'
import { api } from '@/utils/api'
import { useMutation } from '@tanstack/react-query'
import {
    ChannelQueueViewerId,
    QueueViewerCreate,
} from '../types/queue-viewer.types'
import { ChannelQueueId } from '../types/queue.types'
import { getQueueViewersQueryKey } from './queue-viewers.api'

interface CreateProps {
    channelId: ChannelId
    channelQueueId: ChannelQueueId
    data: QueueViewerCreate
}

export async function createQueueViewer({
    channelId,
    channelQueueId,
    data,
}: CreateProps): Promise<QueueViewerCreate> {
    const r = await api.post<QueueViewerCreate>(
        `/api/2/channels/${channelId}/queues/${channelQueueId}/viewers`,
        data
    )
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
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getQueueViewersQueryKey({
                    channelId: variables.channelId,
                    channelQueueId: variables.channelQueueId,
                }),
                data
            )
            queryClient.invalidateQueries({
                queryKey: getQueueViewersQueryKey({
                    channelId: variables.channelId,
                    channelQueueId: variables.channelQueueId,
                }),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface MoveToTopProps {
    channelId: ChannelId
    channelQueueId: ChannelQueueId
    data: {
        channelQueueViewerId: ChannelQueueViewerId
    }
}

export async function moveQueueViewerToTop({
    channelId,
    channelQueueId,
    data,
}: MoveToTopProps): Promise<void> {
    await api.put(
        `/api/2/channels/${channelId}/queues/${channelQueueId}/move-to-top`,
        data
    )
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
        onSuccess: (data, variables) => {
            queryClient.invalidateQueries({
                queryKey: getQueueViewersQueryKey({
                    channelId: variables.channelId,
                    channelQueueId: variables.channelQueueId,
                }),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface DeleteProps {
    channelId: ChannelId
    channelQueueId: ChannelQueueId
    channelQueueViewerId: string
}

export async function deleteQueueViewer({
    channelId,
    channelQueueId,
    channelQueueViewerId,
}: DeleteProps): Promise<void> {
    await api.delete(
        `/api/2/channels/${channelId}/queues/${channelQueueId}/viewers/${channelQueueViewerId}`
    )
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
        onSuccess: (data, variables) => {
            queryClient.invalidateQueries({
                queryKey: getQueueViewersQueryKey({
                    channelId: variables.channelId,
                    channelQueueId: variables.channelQueueId,
                }),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface ClearQueueProps {
    channelId: ChannelId
    channelQueueId: ChannelQueueId
}

export async function clearQueueViewer({
    channelId,
    channelQueueId,
}: ClearQueueProps): Promise<void> {
    await api.delete(
        `/api/2/channels/${channelId}/queues/${channelQueueId}/viewers`
    )
}

export function useClearQueueViewer({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: ClearQueueProps) => void
    onError?: (error: any, variables: ClearQueueProps) => void
} = {}) {
    return useMutation({
        mutationFn: clearQueueViewer,
        onSuccess: (data, variables) => {
            queryClient.invalidateQueries({
                queryKey: getQueueViewersQueryKey({
                    channelId: variables.channelId,
                    channelQueueId: variables.channelQueueId,
                }),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}
