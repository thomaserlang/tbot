import { ChatFilterId } from '@/features/channel-chat-filters/filter.types'
import { ChannelId } from '@/features/channel/types'
import { queryClient } from '@/queryclient'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import { getBannedTermsQueryKey } from './banned-terms.api'
import {
    BannedTerm,
    BannedTermId,
    BannedTermRequest,
} from './banned-terms.types'

export function getBannedTermQueryKey(
    channelId: ChannelId,
    chatFilterId: ChatFilterId,
    bannedTermId: BannedTermId
) {
    return ['banned-term', channelId, chatFilterId, bannedTermId]
}

export async function getBannedTerm(
    channelId: ChannelId,
    chatFilterId: ChatFilterId,
    bannedTermId: BannedTermId
) {
    const r = await api.get<BannedTerm>(
        `/api/2/channels/${channelId}/chat-filters/${chatFilterId}/banned-terms/${bannedTermId}`
    )
    return r.data
}

interface GetProps {
    channelId: ChannelId
    chatFilterId: ChatFilterId
    bannedTermId: BannedTermId
}

export function useGetBannedTerm({
    channelId,
    chatFilterId,
    bannedTermId,
}: GetProps) {
    return useQuery({
        queryKey: getBannedTermQueryKey(channelId, chatFilterId, bannedTermId),
        queryFn: () => getBannedTerm(channelId, chatFilterId, bannedTermId),
    })
}

export async function createBannedTerm(
    channelId: ChannelId,
    chatFilterId: ChatFilterId,
    data: BannedTermRequest
) {
    const r = await api.post<BannedTerm>(
        `/api/2/channels/${channelId}/chat-filters/${chatFilterId}/banned-terms`,
        data
    )
    return r.data
}

interface CreateProps {
    channelId: ChannelId
    chatFilterId: ChatFilterId
    data: BannedTermRequest
}

export function useCreateBannedTerm({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: BannedTerm, variables: CreateProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, chatFilterId, data }: CreateProps) =>
            createBannedTerm(channelId, chatFilterId, data),
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getBannedTermQueryKey(
                    variables.channelId,
                    variables.chatFilterId,
                    data.id
                ),
                data
            )
            queryClient.invalidateQueries({
                queryKey: getBannedTermsQueryKey(
                    variables.channelId,
                    variables.chatFilterId
                ),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

export async function updateBannedTerm(
    channelId: ChannelId,
    chatFilterId: ChatFilterId,
    bannedTermId: BannedTermId,
    data: BannedTermRequest
) {
    const r = await api.put<BannedTerm>(
        `/api/2/channels/${channelId}/chat-filters/${chatFilterId}/banned-terms/${bannedTermId}`,
        data
    )
    return r.data
}

interface UpdateProps {
    channelId: ChannelId
    chatFilterId: ChatFilterId
    bannedTermId: BannedTermId
    data: BannedTermRequest
}

export function useUpdateBannedTerm({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: BannedTerm, variables: UpdateProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: ({
            channelId,
            chatFilterId,
            bannedTermId,
            data,
        }: UpdateProps) =>
            updateBannedTerm(channelId, chatFilterId, bannedTermId, data),
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getBannedTermQueryKey(
                    variables.channelId,
                    variables.chatFilterId,
                    variables.bannedTermId
                ),
                data
            )
            queryClient.invalidateQueries({
                queryKey: getBannedTermsQueryKey(
                    variables.channelId,
                    variables.chatFilterId
                ),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

export async function deleteBannedTerm(
    channelId: ChannelId,
    chatFilterId: ChatFilterId,
    bannedTermId: BannedTermId
) {
    await api.delete<BannedTerm>(
        `/api/2/channels/${channelId}/chat-filters/${chatFilterId}/banned-terms/${bannedTermId}`
    )
}

interface DeleteProps {
    channelId: ChannelId
    chatFilterId: ChatFilterId
    bannedTermId: BannedTermId
}

export function useDeleteBannedTerm({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, chatFilterId, bannedTermId }: DeleteProps) =>
            deleteBannedTerm(channelId, chatFilterId, bannedTermId),
        onSuccess: (data, variables) => {
            queryClient.removeQueries({
                queryKey: getBannedTermQueryKey(
                    variables.channelId,
                    variables.chatFilterId,
                    variables.bannedTermId
                ),
            })
            queryClient.invalidateQueries({
                queryKey: getBannedTermsQueryKey(
                    variables.channelId,
                    variables.chatFilterId
                ),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}
