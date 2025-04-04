import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { useInfiniteQuery } from '@tanstack/react-query'
import { ChannelId } from '../channel/types'
import { Timer } from './timer.types'

interface Params {}

export function getTimersQueryKey(channelId: ChannelId, params?: Params) {
    return ['timers', channelId, params]
}

export async function getTimers(
    channelId: ChannelId,
    params?: Params & { cursor?: string }
) {
    const r = await api.get<PageCursor<Timer>>(
        `/api/2/channels/${channelId}/timers`,
        {
            params,
        }
    )
    return r.data
}

export function useGetTimers(channelId: ChannelId, params?: Params) {
    return useInfiniteQuery({
        queryKey: getTimersQueryKey(channelId, params),
        queryFn: ({ pageParam }) =>
            getTimers(channelId, { ...params, cursor: pageParam }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
    })
}
