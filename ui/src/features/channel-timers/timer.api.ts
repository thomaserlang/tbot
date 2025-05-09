import { queryClient } from '@/queryclient'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import { ChannelId } from '../channel/types/channel.types'
import { Timer, TimerCreate, TimerId, TimerUpdate } from './timer.types'
import { getTimersQueryKey } from './timers.api'

export function getTimerQueryKey(timerId: TimerId) {
    return ['timer', timerId]
}

export async function getTimer(channelId: ChannelId, timerId: TimerId) {
    const r = await api.get<Timer>(
        `/api/2/channels/${channelId}/timers/${timerId}`
    )
    return r.data
}

interface Props {
    channelId: ChannelId
    timerId: TimerId
}
export function useGetTimer({ channelId, timerId }: Props) {
    return useQuery({
        queryKey: getTimerQueryKey(timerId),
        queryFn: () => getTimer(channelId, timerId),
        enabled: !!channelId && !!timerId,
    })
}

export async function createTimer(channelId: ChannelId, data: TimerCreate) {
    const r = await api.post<Timer>(`/api/2/channels/${channelId}/timers`, data)
    return r.data
}

interface CreateProps {
    channelId: ChannelId
    data: TimerCreate
}

export function useCreateTimer({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: Timer, variables: CreateProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, data }: CreateProps) =>
            createTimer(channelId, data),
        onSuccess: (data, variables) => {
            queryClient.setQueryData(getTimerQueryKey(data.id), data)
            queryClient.invalidateQueries({
                queryKey: getTimersQueryKey(variables.channelId),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

export async function updateTimer(
    channelId: ChannelId,
    timerId: TimerId,
    data: TimerUpdate
) {
    const r = await api.put<Timer>(
        `/api/2/channels/${channelId}/timers/${timerId}`,
        data
    )
    return r.data
}

interface UpdateProps {
    channelId: ChannelId
    timerId: TimerId
    data: TimerUpdate
}
export function useUpdateTimer({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: Timer, variables: UpdateProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, timerId, data }: UpdateProps) =>
            updateTimer(channelId, timerId, data),
        onSuccess: (data, variables) => {
            queryClient.setQueryData(getTimerQueryKey(data.id), data)
            queryClient.invalidateQueries({
                queryKey: getTimersQueryKey(variables.channelId),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

export async function deleteTimer(
    channelId: ChannelId,
    timerId: TimerId
): Promise<void> {
    await api.delete(`/api/2/channels/${channelId}/timers/${timerId}`)
}

interface DeleteProps {
    channelId: ChannelId
    timerId: TimerId
}

export function useDeleteTimer({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, timerId }: DeleteProps) =>
            deleteTimer(channelId, timerId),
        onSuccess: (data, variables) => {
            queryClient.removeQueries({
                queryKey: getTimerQueryKey(variables.timerId),
            })
            queryClient.invalidateQueries({
                queryKey: getTimersQueryKey(variables.channelId),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}
