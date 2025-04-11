import { ProviderBot } from '@/features/provider-bot/provider-bot.types'
import { queryClient } from '@/queryclient'
import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import { getSystemProviderBotsQueryKey } from './provider-bots.api'

export function getSystemProviderBotQueryKey(provider: Provider) {
    return ['botProvider', provider]
}

export async function getSystemProviderBot(provider: Provider) {
    const r = await api.get<ProviderBot>(
        `/api/2/system-bot-providers/${provider}`
    )
    return r.data
}

interface GetParams {
    provider: Provider
}
export function useGetSystemProviderBot(props: GetParams) {
    return useQuery({
        queryKey: getSystemProviderBotQueryKey(props.provider),
        queryFn: () => getSystemProviderBot(props.provider),
    })
}

export async function deleteSystemProvider(provider: Provider) {
    await api.delete(`/api/2/system-bot-providers/${provider}`)
}

interface DeleteParams {
    provider: Provider
}

export function useDeleteSystemProviderBot({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteParams) => void
    onError?: (error: unknown) => void
} = {}) {
    return useMutation({
        mutationFn: async ({ provider }: DeleteParams) => {
            await deleteSystemProvider(provider)
        },
        onSuccess: (data, variables) => {
            queryClient.removeQueries({
                queryKey: getSystemProviderBotQueryKey(variables.provider),
            })
            queryClient.setQueryData(
                getSystemProviderBotsQueryKey(),
                (oldData: ProviderBot[]) =>
                    oldData.filter(
                        (provider) => provider.provider !== variables.provider
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

export function useGetSystemProviderBotConnectUrl({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ConnectURL) => void
    onError?: (error: unknown) => void
} = {}) {
    return useMutation({
        mutationFn: async ({ provider }: { provider: Provider }) => {
            const r = await api.get<ConnectURL>(
                `/api/2/${provider}/system-provider-bot-connect-url`
            )
            return r.data
        },
        onSuccess,
        onError,
    })
}
