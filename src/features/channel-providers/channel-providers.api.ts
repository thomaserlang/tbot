import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { ChannelId } from '../channel/types'
import { ChannelProvider } from './channel-providers.types'

interface Props {
    channelId: ChannelId
}

export function getChannelProvidersQueryKey(props: Props) {
    return ['channelProviders', props.channelId]
}

export async function getChannelProviders(props: Props) {
    const r = await api.get<ChannelProvider[]>(
        `/api/2/channels/${props.channelId}/providers`
    )
    return r.data
}

export function useGetChannelProviders(props: Props) {
    return useQuery({
        queryKey: getChannelProvidersQueryKey(props),
        queryFn: () => getChannelProviders(props),
    })
}
