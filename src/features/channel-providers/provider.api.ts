import { ChannelId } from '@/features/channel/types'
import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import { ChannelProvider, ChannelProviderId } from './provider.types'

export function getProviderQueryKey(
    channelId: ChannelId,
    providerId: ChannelProviderId
) {
    return ['channelProvider', channelId, providerId]
}

export async function getProvider(
    channelId: ChannelId,
    providerId: ChannelProviderId
) {
    const r = await api.get<ChannelProvider>(
        `/api/2/channels/${channelId}/providers/${providerId}`
    )
    return r.data
}

interface GetParams {
    channelId: ChannelId
    providerId: ChannelProviderId
}
export function useGetProvider(props: GetParams) {
    return useQuery({
        queryKey: getProviderQueryKey(props.channelId, props.providerId),
        queryFn: () => getProvider(props.channelId, props.providerId),
    })
}

export function useGetProviderConnectUrl({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: { url: string }) => void
    onError?: (error: unknown) => void
} = {}) {
    return useMutation({
        mutationFn: async ({
            channelId,
            provider,
        }: {
            channelId: ChannelId
            provider: Provider
        }) => {
            const r = await api.get<{
                url: string
            }>(`/api/2/channels/${channelId}/${provider}/connect-url`)
            return r.data
        },
        onSuccess,
        onError,
    })
}
