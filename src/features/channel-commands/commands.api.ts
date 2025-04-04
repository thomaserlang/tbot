import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { useInfiniteQuery } from '@tanstack/react-query'
import { ChannelId } from '../channel/types'
import { Command } from './command.types'

interface IParams {}

export function getCommandsQueryKey(channelId: ChannelId, params?: IParams) {
    return ['commands', channelId, params]
}

export async function getCommands(
    channelId: ChannelId,
    params?: IParams & { cursor?: string }
) {
    const r = await api.get<PageCursor<Command>>(
        `/api/2/channels/${channelId}/commands`,
        {
            params,
        }
    )
    return r.data
}

export function useGetCommands(channelId: ChannelId, params?: IParams) {
    return useInfiniteQuery({
        queryKey: getCommandsQueryKey(channelId, params),
        queryFn: ({ pageParam }) =>
            getCommands(channelId, { ...params, cursor: pageParam }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
    })
}
