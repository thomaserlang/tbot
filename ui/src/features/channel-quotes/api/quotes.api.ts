import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { useInfiniteQuery } from '@tanstack/react-query'
import { ChannelQuote } from '../types/quote.types'

interface GetParams {}

interface GetProps {
    channelId: string
    params?: GetParams
}

export function getQuotesQueryKey({ channelId, params }: GetProps) {
    return ['channel-quotes', channelId, params]
}

export async function getQuotes({
    channelId,
    params,
}: GetProps & { params?: GetParams & { cursor?: string } }) {
    const r = await api.get<PageCursor<ChannelQuote>>(
        `/api/2/channels/${channelId}/quotes`,
        { params }
    )
    return r.data
}

export function useGetQuotes({ channelId, params }: GetProps) {
    return useInfiniteQuery({
        queryKey: getQuotesQueryKey({ channelId }),
        queryFn: ({ pageParam }) =>
            getQuotes({
                channelId,
                params: {
                    ...params,
                    cursor: pageParam,
                },
            }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor,
    })
}
