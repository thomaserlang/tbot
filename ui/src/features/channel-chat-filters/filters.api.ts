import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { ChannelId } from '../channel/types/channel.types'
import { ChatFilter } from './filter-registry'

interface Params {}

export function getChatFiltersQueryKey(channelId: ChannelId, params?: Params) {
    return ['chat-filters', channelId, params]
}

export async function getChatFilters(channelId: ChannelId, params?: Params) {
    const r = await api.get<ChatFilter[]>(
        `/api/2/channels/${channelId}/chat-filters`,
        {
            params,
        }
    )
    return r.data
}

interface Props {
    channelId: ChannelId
    params?: Params
}

export function useGetChatFilters({ channelId, params }: Props) {
    return useQuery({
        queryKey: getChatFiltersQueryKey(channelId, params),
        queryFn: () => getChatFilters(channelId, params),
        enabled: Boolean(channelId),
    })
}
