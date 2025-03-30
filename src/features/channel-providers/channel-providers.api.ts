import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { IChannelProvider } from './channel-providers.types'

interface IParams {
    channelId: string
}

export function getChannelProvidersQueryKey(props: IParams) {
    return ['channelProviders', props.channelId]
}

export async function getChannelProviders(props: IParams) {
    const r = await api.get<IChannelProvider[]>(
        `/api/2/channels/${props.channelId}/providers`
    )
    return r.data
}

export function useGetChannelProviders(props: IParams) {
    return useQuery({
        queryKey: getChannelProvidersQueryKey(props),
        queryFn: () => getChannelProviders(props),
    })
}
