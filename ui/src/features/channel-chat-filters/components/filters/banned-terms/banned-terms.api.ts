import { ChannelId } from '@/features/channel/types'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { useInfiniteQuery, useMutation } from '@tanstack/react-query'
import { ChatFilterId, ChatFilterMatchResult } from '../../../filter.types'
import { BannedTerm } from './banned-terms.types'

interface Params {}

export function getBannedTermsQueryKey(
    channelId: ChannelId,
    chatFilterId: ChatFilterId,
    params?: Params
) {
    return ['banned-terms', channelId, chatFilterId, params]
}

export async function getBannedTerms(
    channelId: ChannelId,
    chatFilterId: ChatFilterId,
    params: Params & { cursor?: string } = {}
) {
    const r = await api.get<PageCursor<BannedTerm>>(
        `/api/2/channels/${channelId}/chat-filters/${chatFilterId}/banned-terms`,
        {
            params,
        }
    )
    return r.data
}

interface GetProps {
    channelId: ChannelId
    chatFilterId: ChatFilterId
    params?: Params
}

export function useGetBannedTerms({
    channelId,
    chatFilterId,
    params,
}: GetProps) {
    return useInfiniteQuery({
        queryKey: getBannedTermsQueryKey(channelId, chatFilterId),
        queryFn: ({ pageParam }) =>
            getBannedTerms(channelId, chatFilterId, {
                ...params,
                cursor: pageParam,
            }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
    })
}

export async function testTestBannedTerms(
    channelId: ChannelId,
    chatFilterId: ChatFilterId,
    message: string
) {
    const r = await api.post<ChatFilterMatchResult>(
        `/api/2/channels/${channelId}/chat-filters/${chatFilterId}/banned-terms/test`,
        {
            message,
        }
    )
    return r.data
}

interface TestProps {
    channelId: ChannelId
    chatFilterId: ChatFilterId
    message: string
}

export function useTestBannedTerms({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChatFilterMatchResult, variables: TestProps) => void
    onError?: (error: unknown) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, chatFilterId, message }) =>
            testTestBannedTerms(channelId, chatFilterId, message),
        onSuccess,
        onError,
    })
}
