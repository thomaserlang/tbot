import { ChannelId } from '@/features/channel/types'
import { queryClient } from '@/queryclient'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { removeRecord, updateRecord } from '@/utils/page-records'
import { InfiniteData, useMutation, useQuery } from '@tanstack/react-query'
import {
    ChannelQuote,
    ChannelQuoteCreate,
    ChannelQuoteId,
    ChannelQuoteUpdate,
} from '../types/quote.types'
import { getQuotesQueryKey } from './quotes.api'

interface GetProps {
    channelId: ChannelId
    channelQuoteId: ChannelQuoteId
}

export function getQuoteQueryKey({ channelId, channelQuoteId }: GetProps) {
    return ['channel-quote', channelId, channelQuoteId]
}

export async function getChannelQuote({ channelId, channelQuoteId }: GetProps) {
    const r = await api.get<ChannelQuote>(
        `/api/2/channels/${channelId}/quotes/${channelQuoteId}`
    )
    return r.data
}

export function useGetQuote({ channelId, channelQuoteId }: GetProps) {
    return useQuery({
        queryKey: getQuoteQueryKey({ channelId, channelQuoteId }),
        queryFn: () => getChannelQuote({ channelId, channelQuoteId }),
    })
}

interface CreateProps {
    channelId: ChannelId
    data: ChannelQuoteCreate
}

export async function createQuote({ channelId, data }: CreateProps) {
    const r = await api.post<ChannelQuote>(
        `/api/2/channels/${channelId}/quotes`,
        data
    )
    return r.data
}

export function useCreateQuote({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChannelQuote, variables: CreateProps) => void
    onError?: (error: any, variables: CreateProps) => void
} = {}) {
    return useMutation({
        mutationFn: createQuote,
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getQuoteQueryKey({
                    channelId: variables.channelId,
                    channelQuoteId: data.id,
                }),
                data
            )
            queryClient.invalidateQueries({
                queryKey: getQuotesQueryKey({
                    channelId: variables.channelId,
                }),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface UpdateProps {
    channelId: ChannelId
    channelQuoteId: ChannelQuoteId
    data: ChannelQuoteUpdate
}

export async function updateQuote({
    channelId,
    channelQuoteId,
    data,
}: UpdateProps) {
    const r = await api.put<ChannelQuote>(
        `/api/2/channels/${channelId}/quotes/${channelQuoteId}`,
        data
    )
    return r.data
}

export function useUpdateQuote({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChannelQuote, variables: UpdateProps) => void
    onError?: (error: any, variables: UpdateProps) => void
} = {}) {
    return useMutation({
        mutationFn: updateQuote,
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getQuoteQueryKey({
                    channelId: variables.channelId,
                    channelQuoteId: data.id,
                }),
                data
            )
            queryClient.setQueryData(
                getQuotesQueryKey({
                    channelId: variables.channelId,
                }),
                (oldData: InfiniteData<PageCursor<ChannelQuote>>) =>
                    updateRecord(oldData, data, (item) => item.id === data.id)
            )
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface DeleteProps {
    channelId: ChannelId
    channelQuoteId: ChannelQuoteId
}
export async function deleteQuote({ channelId, channelQuoteId }: DeleteProps) {
    const r = await api.delete(
        `/api/2/channels/${channelId}/quotes/${channelQuoteId}`
    )
    return r.data
}

export function useDeleteQuote({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: any, variables: DeleteProps) => void
} = {}) {
    return useMutation({
        mutationFn: deleteQuote,
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getQuotesQueryKey({
                    channelId: variables.channelId,
                }),
                (oldData: InfiniteData<PageCursor<ChannelQuote>>) =>
                    removeRecord(
                        oldData,
                        (item) => item.id !== variables.channelQuoteId
                    )
            )
            queryClient.removeQueries({
                queryKey: getQuoteQueryKey({
                    channelId: variables.channelId,
                    channelQuoteId: variables.channelQuoteId,
                }),
            })
            queryClient.invalidateQueries({
                queryKey: getQuotesQueryKey({
                    channelId: variables.channelId,
                }),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}
