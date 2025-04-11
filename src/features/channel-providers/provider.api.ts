import { ChannelId } from '@/features/channel/types'
import { queryClient } from '@/queryclient'
import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import { useLocation } from 'react-router-dom'
import { ChannelProvider, ChannelProviderId } from './provider.types'
import { getProvidersQueryKey } from './providers.api'

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

export async function deleteProvider(
    channelId: ChannelId,
    providerId: ChannelProviderId
) {
    await api.delete(`/api/2/channels/${channelId}/providers/${providerId}`)
}

interface DeleteParams {
    channelId: ChannelId
    providerId: ChannelProviderId
}

export function useDeleteProvider({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteParams) => void
    onError?: (error: unknown) => void
} = {}) {
    return useMutation({
        mutationFn: async ({ channelId, providerId }: DeleteParams) => {
            await deleteProvider(channelId, providerId)
        },
        onSuccess: (data, variables) => {
            queryClient.removeQueries({
                queryKey: getProviderQueryKey(
                    variables.channelId,
                    variables.providerId
                ),
            })
            queryClient.setQueryData(
                getProvidersQueryKey(variables.channelId),
                (oldData: ChannelProvider[]) =>
                    oldData.filter(
                        (provider) => provider.id !== variables.providerId
                    )
            )
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface ConnectURL {
    url: string
}

export function useGetProviderConnectUrl({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ConnectURL) => void
    onError?: (error: unknown) => void
} = {}) {
    const location = useLocation()
    return useMutation({
        mutationFn: async ({
            channelId,
            provider,
        }: {
            channelId: ChannelId
            provider: Provider
        }) => {
            const r = await api.get<ConnectURL>(
                `/api/2/channels/${channelId}/${provider}/connect-url`,
                {
                    params: {
                        redirect_to: location.pathname + location.search,
                    },
                }
            )
            return r.data
        },
        onSuccess,
        onError,
    })
}

export function useGetProviderConnectBotUrl({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ConnectURL) => void
    onError?: (error: unknown) => void
} = {}) {
    const location = useLocation()
    return useMutation({
        mutationFn: async ({
            channelId,
            provider,
        }: {
            channelId: ChannelId
            provider: Provider
        }) => {
            const r = await api.get<ConnectURL>(
                `/api/2/channels/${channelId}/${provider}/connect-bot-url`,
                {
                    params: {
                        redirect_to: location.pathname + location.search,
                    },
                }
            )
            return r.data
        },
        onSuccess,
        onError,
    })
}

export async function disconnectProviderBot(
    channelId: ChannelId,
    providerId: ChannelProviderId
) {
    await api.delete(`/api/2/channels/${channelId}/providers/${providerId}/bot`)
}

interface DisconnectBotParams {
    channelId: ChannelId
    providerId: ChannelProviderId
}
export function useDisconnectProviderBot({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DisconnectBotParams) => void
    onError?: (error: unknown) => void
} = {}) {
    return useMutation({
        mutationFn: async ({ channelId, providerId }: DisconnectBotParams) => {
            await disconnectProviderBot(channelId, providerId)
        },
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getProviderQueryKey(variables.channelId, variables.providerId),
                (oldData: ChannelProvider) => ({
                    ...oldData,
                    bot_provider: null,
                })
            )
            queryClient.setQueryData(
                getProvidersQueryKey(variables.channelId),
                (oldData: ChannelProvider[]) =>
                    oldData.map((provider) =>
                        provider.id === variables.providerId
                            ? { ...provider, bot_provider: null }
                            : provider
                    )
            )
            onSuccess?.(data, variables)
        },
        onError,
    })
}
