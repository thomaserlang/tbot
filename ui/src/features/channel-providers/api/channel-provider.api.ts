import { ChannelId } from '@/features/channel/types'
import { queryClient } from '@/queryclient'
import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import { useLocation } from 'react-router-dom'
import { ChannelProvider, ChannelProviderId } from '../channel-provider.types'
import { getChannelProvidersQueryKey } from './channel-providers.api'

export function getChannelProviderQueryKey(
    channelId: ChannelId,
    providerId: ChannelProviderId
) {
    return ['channelProvider', channelId, providerId]
}

export async function getChannelProvider(
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
    channelProviderId: ChannelProviderId
}
export function useGetChannelProvider(props: GetParams) {
    return useQuery({
        queryKey: getChannelProviderQueryKey(
            props.channelId,
            props.channelProviderId
        ),
        queryFn: () =>
            getChannelProvider(props.channelId, props.channelProviderId),
    })
}

export async function deleteChannelProvider(
    channelId: ChannelId,
    channelProviderId: ChannelProviderId
) {
    await api.delete(
        `/api/2/channels/${channelId}/providers/${channelProviderId}`
    )
}

interface DeleteParams {
    channelId: ChannelId
    channelProviderId: ChannelProviderId
}

export function useDeleteChannelProvider({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteParams) => void
    onError?: (error: unknown) => void
} = {}) {
    return useMutation({
        mutationFn: async ({
            channelId,
            channelProviderId: providerId,
        }: DeleteParams) => {
            await deleteChannelProvider(channelId, providerId)
        },
        onSuccess: (data, variables) => {
            queryClient.removeQueries({
                queryKey: getChannelProviderQueryKey(
                    variables.channelId,
                    variables.channelProviderId
                ),
            })
            queryClient.setQueryData(
                getChannelProvidersQueryKey(variables.channelId),
                (oldData: ChannelProvider[]) =>
                    oldData.filter(
                        (provider) =>
                            provider.id !== variables.channelProviderId
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

export function useGetChannelProviderConnectUrl({
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

export function useGetChannelProviderConnectBotUrl({
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

export async function disconnectChannelProviderBot(
    channelId: ChannelId,
    providerId: ChannelProviderId
) {
    await api.delete(`/api/2/channels/${channelId}/providers/${providerId}/bot`)
}

interface DisconnectBotParams {
    channelId: ChannelId
    providerId: ChannelProviderId
}
export function useDisconnectChannelProviderBot({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DisconnectBotParams) => void
    onError?: (error: unknown) => void
} = {}) {
    return useMutation({
        mutationFn: async ({ channelId, providerId }: DisconnectBotParams) => {
            await disconnectChannelProviderBot(channelId, providerId)
        },
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getChannelProviderQueryKey(
                    variables.channelId,
                    variables.providerId
                ),
                (oldData: ChannelProvider) => ({
                    ...oldData,
                    bot_provider: null,
                })
            )
            queryClient.setQueryData(
                getChannelProvidersQueryKey(variables.channelId),
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

export function updateChannelProviderCache(channelProvider: ChannelProvider) {
    queryClient.setQueryData(
        getChannelProviderQueryKey(
            channelProvider.channel_id,
            channelProvider.id
        ),
        channelProvider
    )
    queryClient.setQueryData(
        getChannelProvidersQueryKey(channelProvider.channel_id),
        (oldData: ChannelProvider[]) =>
            oldData.map((provider) =>
                provider.id === channelProvider.id ? channelProvider : provider
            )
    )
}
