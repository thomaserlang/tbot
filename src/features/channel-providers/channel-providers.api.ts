import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { ChannelId } from '../channel/types'
import { ChannelProvider } from './channel-provider.types'

export function getChannelProvidersQueryKey(channelId: ChannelId) {
    return ['channelProviders', channelId]
}

export async function getChannelProviders(channelId: ChannelId) {
    const r = await api.get<ChannelProvider[]>(
        `/api/2/channels/${channelId}/providers`
    )
    return r.data
}

interface GetProps {
    channelId: ChannelId
    options?: {
        refetchInterval?: number
    }
}

export function useGetChannelProviders(props: GetProps) {
    return useQuery({
        queryKey: getChannelProvidersQueryKey(props.channelId),
        queryFn: () => getChannelProviders(props.channelId),
        ...props.options,
    })
}
