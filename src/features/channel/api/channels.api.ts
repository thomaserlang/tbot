import { IPageCursor } from '@/types/page-cursor'
import { api } from '@/utils/api'
import { useInfiniteQuery } from '@tanstack/react-query'
import { IChannel } from '../types'

interface IParams {
    name?: string
}

export function getChannelsQueryKey(params: IParams) {
    return ['channels', params]
}

export async function getChannels(params: IParams & { cursor?: string } = {}) {
    const r = await api.get<IPageCursor<IChannel>>('/api/2/channels', {
        params: params,
    })
    return r.data
}

export function useGetChannels(params: IParams = {}) {
    return useInfiniteQuery({
        queryKey: getChannelsQueryKey(params),
        queryFn: async ({ pageParam }) =>
            await getChannels({ ...params, cursor: pageParam }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
    })
}
