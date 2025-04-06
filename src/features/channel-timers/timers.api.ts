import { getAllPagesCursor } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
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
    const r = await getAllPagesCursor<Timer>(
        `/api/2/channels/${channelId}/timers`,
        {
            params,
        }
    )
    return r
}

export function useGetTimers(channelId: ChannelId, params?: Params) {
    return useQuery({
        queryKey: getTimersQueryKey(channelId, params),
        queryFn: () => getTimers(channelId, params),
    })
}
