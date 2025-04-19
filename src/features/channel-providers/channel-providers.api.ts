import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { ChannelId } from '../channel/types'
import { ChannelProvider } from './channel-provider.types'

export function getProvidersQueryKey(channelId: ChannelId) {
    return ['channelProviders', channelId]
}

export async function getProviders(channelId: ChannelId) {
    const r = await api.get<ChannelProvider[]>(
        `/api/2/channels/${channelId}/providers`
    )
    return r.data
}

interface GetParams {
    channelId: ChannelId
}

export function useGetProviders(props: GetParams) {
    return useQuery({
        queryKey: getProvidersQueryKey(props.channelId),
        queryFn: () => getProviders(props.channelId),
    })
}
