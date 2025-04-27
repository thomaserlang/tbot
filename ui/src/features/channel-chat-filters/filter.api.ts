import { ChannelId } from '@/features/channel/types'
import { queryClient } from '@/queryclient'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import { ChatFilter, ChatFilterRequest } from './filter-registry'
import { ChatFilterId } from './filter.types'
import { getChatFiltersQueryKey } from './filters.api'

export function getChatFilterQueryKey(filterId: ChatFilterId) {
    return ['filter', filterId]
}

export async function getChatFilter(
    channelId: ChannelId,
    filterId: ChatFilterId
) {
    const r = await api.get<ChatFilter>(
        `/api/2/channels/${channelId}/chat-filters/${filterId}`
    )
    return r.data
}

interface Props {
    channelId: ChannelId
    filterId: ChatFilterId
}

export function useGetChatFilter({ channelId, filterId }: Props) {
    return useQuery({
        queryKey: getChatFilterQueryKey(filterId),
        queryFn: () => getChatFilter(channelId, filterId),
        enabled: Boolean(channelId && filterId),
    })
}

export async function createChatFilter(
    channelId: ChannelId,
    data: ChatFilterRequest
) {
    const r = await api.post<ChatFilter>(
        `/api/2/channels/${channelId}/chat-filters`,
        data
    )
    return r.data
}

interface CreateProps {
    channelId: ChannelId
    data: ChatFilterRequest
}

export function useCreateChatFilter({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChatFilter, variables: CreateProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, data }: CreateProps) =>
            createChatFilter(channelId, data),
        onSuccess: (data, variables) => {
            queryClient.setQueryData(getChatFilterQueryKey(data.id), data)
            queryClient.setQueryData(
                getChatFiltersQueryKey(variables.channelId),
                (oldData: ChatFilter[]) => {
                    if (!oldData) return [data]
                    return [data, ...oldData]
                }
            )
            onSuccess?.(data, variables)
        },
        onError: onError,
    })
}

export async function updateChatFilter(
    channelId: ChannelId,
    filterId: ChatFilterId,
    data: ChatFilterRequest
) {
    const r = await api.put<ChatFilter>(
        `/api/2/channels/${channelId}/chat-filters/${filterId}`,
        data
    )
    return r.data
}

interface UpdateProps {
    channelId: ChannelId
    filterId: ChatFilterId
    data: ChatFilterRequest
}

export function useUpdateChatFilter({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChatFilter, variables: UpdateProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, filterId, data }: UpdateProps) =>
            updateChatFilter(channelId, filterId, data),
        onSuccess: (data, variables) => {
            queryClient.setQueryData(getChatFilterQueryKey(data.id), data)
            queryClient.setQueryData(
                getChatFiltersQueryKey(variables.channelId),
                (oldData: ChatFilter[]) => [
                    ...oldData.map((f) => (f.id === data.id ? data : f)),
                ]
            )
            onSuccess?.(data, variables)
        },
        onError: onError,
    })
}

export async function deleteChatFilter(
    channelId: ChannelId,
    filterId: ChatFilterId
) {
    await api.delete(`/api/2/channels/${channelId}/chat-filters/${filterId}`)
}

interface DeleteProps {
    channelId: ChannelId
    filterId: ChatFilterId
}
export function useDeleteChatFilter({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, filterId }: DeleteProps) =>
            deleteChatFilter(channelId, filterId),
        onSuccess: (data, variables) => {
            queryClient.removeQueries({
                queryKey: getChatFilterQueryKey(variables.filterId),
            })
            queryClient.setQueryData(
                getChatFiltersQueryKey(variables.channelId),
                (oldData: ChatFilter[]) =>
                    oldData.filter((f) => f.id !== variables.filterId)
            )
            onSuccess?.(data, variables)
        },
        onError: onError,
    })
}
